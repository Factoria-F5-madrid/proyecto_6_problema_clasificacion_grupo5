import argparse
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, log_loss
from lightgbm import LGBMClassifier
import os
import json
import random
import glob # to help with flexible file loading

SEED = 42 # for reproducibility

def set_seed(seed=SEED):
    np.random.seed(seed)
    random.seed(seed)


def load_data(path, target_col=None):
    """
    Flexible loader:
      - Accepts a file path (csv or parquet) OR a directory path containing a csv/parquet.
      - If target_col is provided, uses that column as the label.
      - If target_col is None, tries common names and simple heuristics to detect a label column.
    """
    import os
    import pandas as pd
    import glob

    def _read_file(p):
        if p.endswith(".csv"):
            return pd.read_csv(p)
        elif p.endswith(".parquet"):
            return pd.read_parquet(p)
        else:
            # fallback: try by reading as csv
            return pd.read_csv(p)

    # Resolve path -> df (file or directory)
    if os.path.isdir(path):
        csvs = sorted(glob.glob(os.path.join(path, "*.csv")))
        parqs = sorted(glob.glob(os.path.join(path, "*.parquet")))
        candidates = csvs + parqs
        if not candidates:
            raise FileNotFoundError(f"No .csv or .parquet files found in directory: {path}.")
        if len(candidates) > 1:
            print(f"⚠️  Warning: multiple candidate files found in {path}. Picking: {candidates[0]}")
        df = _read_file(candidates[0])
    elif os.path.exists(path):
        df = _read_file(path)
    else:
        # try swaps and common dirs like data/processed
        base, ext = os.path.splitext(path)
        alt = base + (".parquet" if ext.lower() == ".csv" else ".csv")
        if os.path.exists(alt):
            print(f"⚠️  Warning: requested '{path}' not found — loaded '{alt}' instead.")
            df = _read_file(alt)
        else:
            data_dir = os.path.join(os.getcwd(), "data", "processed")
            if os.path.isdir(data_dir):
                csvs = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
                parqs = sorted(glob.glob(os.path.join(data_dir, "*.parquet")))
                candidates = csvs + parqs
                if candidates:
                    print(f"⚠️  Warning: '{path}' not found — loading first candidate from data/processed: {candidates[0]}")
                    df = _read_file(candidates[0])
                else:
                    cwd = os.getcwd()
                    raise FileNotFoundError(f"Data file not found: '{path}'. Current cwd: {cwd}. Contents of ./data: {os.listdir(os.path.join(cwd,'data')) if os.path.exists(os.path.join(cwd,'data')) else 'N/A'}")
            else:
                cwd = os.getcwd()
                raise FileNotFoundError(f"Data file not found: '{path}'. Current cwd: {cwd}. Contents of ./data: {os.listdir(os.path.join(cwd,'data')) if os.path.exists(os.path.join(cwd,'data')) else 'N/A'}")

    # If target_col explicitly provided, check it exists
    if target_col:
        if target_col not in df.columns:
            raise KeyError(f"Requested target column '{target_col}' not found in file. Available columns: {list(df.columns)}")
        y = df[target_col]
        X = df.drop(columns=[target_col])
        return X, y

    # Try common column names
    common_names = ["target", "label", "y", "class", "satisfaction", "is_satisfied", "survived"]
    for name in common_names:
        if name in df.columns:
            print(f"⚠️  Using detected target column: '{name}'")
            y = df[name]
            X = df.drop(columns=[name])
            return X, y

    # Heuristic: look for binary/int columns with small unique counts (<=10)
    candidate_cols = []
    for c in df.columns:
        try:
            nunique = df[c].nunique(dropna=True)
        except Exception:
            nunique = None
        if nunique is not None and nunique <= 10 and df[c].dtype.kind in ("i", "u", "b", "O", "S"):
            candidate_cols.append((c, nunique))
    # sort by smallest unique count first
    candidate_cols = sorted(candidate_cols, key=lambda x: x[1])
    if candidate_cols:
        chosen = candidate_cols[0][0]
        print(f"⚠️  Heuristic chose '{chosen}' as target (unique values: {candidate_cols[0][1]}). If this is wrong, re-run with --target-col <colname>.")
        y = df[chosen]
        X = df.drop(columns=[chosen])
        return X, y

    # Nothing found — helpful error listing columns
    raise KeyError(
        "Could not find a target column. Please pass the column name with --target-col.\n"
        f"Available columns: {list(df.columns)}\n"
        "Example: python src/train_lightgbm.py --data-path data/airline_passenger_satisfaction.csv --target-col satisfaction"
    )



def cross_val_train(X, y, params, n_splits=5, fillna_value=0):
    """
    Cross-val robusto compatible con múltiples versiones de lightgbm:
      - limpia NaNs, convierte object -> category y label-encodea y si hace falta
      - filtra kwargs según la firma de LGBMClassifier.fit para evitar TypeError
      - imprime diagnósticos útiles si algo falla
    """
    import inspect
    import lightgbm as lgb
    from sklearn.preprocessing import LabelEncoder

    # Chequeos y preprocesado ligero
    if len(X) != len(y):
        raise ValueError(f"Length mismatch: X {len(X)} rows vs y {len(y)} rows")

    X = X.copy()
    y = pd.Series(y).copy()

    if X.isnull().any().any():
        X = X.fillna(fillna_value)
        print("⚠️  Warning: NaNs found in X. Filled with:", fillna_value)

    # convertir object a category
    cat_cols = list(X.select_dtypes(include=["object"]).columns)
    if cat_cols:
        for c in cat_cols:
            X[c] = X[c].astype("category")
        print(f"⚠️  Converted object cols to category: {cat_cols}")

    # label-encode si y no es numérico
    if not np.issubdtype(y.dtype, np.number):
        le = LabelEncoder()
        y = pd.Series(le.fit_transform(y), name=y.name)
        print(f"⚠️  Label-encoded y. Classes: {list(le.classes_)}")

    if len(pd.Series(y).unique()) < 2:
        raise ValueError(f"y has {len(pd.Series(y).unique())} unique class(es). Need >=2 classes for stratified CV.")

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    oof_preds = np.zeros(len(y))
    val_scores = []
    models = []

    # función helper: filtra kwargs según la firma de func
    def _filter_kwargs(func, kwargs):
        sig = inspect.signature(func)
        params = sig.parameters
        # si acepta **kwargs, devolvemos todo
        if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()):
            return kwargs
        allowed = {name for name, p in params.items() if p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)}
        return {k: v for k, v in kwargs.items() if k in allowed}

    for fold, (tr_idx, val_idx) in enumerate(skf.split(X, y)):
        X_tr, X_val = X.iloc[tr_idx], X.iloc[val_idx]
        y_tr, y_val = y.iloc[tr_idx], y.iloc[val_idx]

        model = LGBMClassifier(**params, random_state=SEED, n_jobs=-1)

        # candidate kwargs que queremos pasar (algunos pueden no ser soportados por la versión instalada)
        cat_feats = [c for c in X_tr.columns if str(X_tr[c].dtype) == "category"]
        candidate_kwargs = {
            "eval_set": [(X_val, y_val)],
            "early_stopping_rounds": 100,
            "eval_metric": "auc",
            # "verbose" intentionally not required; some versions accept it, others not
            # we'll include it candidate-wise but normally it's not necessary
            # "verbose": False,
        }
        # añadimos callbacks si la librería lo soporta
        callbacks = []
        if hasattr(lgb, "early_stopping"):
            try:
                callbacks.append(lgb.early_stopping(100))
            except Exception:
                callbacks = []
        if callbacks:
            candidate_kwargs["callbacks"] = callbacks

        # también intentaremos pasar categorical_feature si la firma lo acepta
        if cat_feats:
            candidate_kwargs["categorical_feature"] = cat_feats

        # Filtramos kwargs según la firma real de model.fit
        fit_kwargs = _filter_kwargs(model.fit, candidate_kwargs)

        tried_modes = []
        success = False
        # Intentar entrenar con los kwargs filtrados
        try:
            tried_modes.append(f"fit_kwargs_keys={sorted(list(fit_kwargs.keys()))}")
            model.fit(X_tr, y_tr, **fit_kwargs)
            success = True
        except Exception as e:
            # Si falla, imprimimos diagnóstico y reintentamos con un fallback mínimo (sin kwargs)
            print(f"Exception when calling fit with keys {sorted(list(fit_kwargs.keys()))} on fold {fold}: {e}")
            import traceback
            traceback.print_exc()

        if not success:
            # última opción: fit sin kwargs (compatibilidad máxima)
            try:
                tried_modes.append("fit(no kwargs)")
                model.fit(X_tr, y_tr)
                success = True
            except Exception as e:
                print("=== Exception during model.fit fallback in fold", fold, "===")
                print("Tried modes:", tried_modes)
                print("Shapes -> X_tr:", X_tr.shape, " X_val:", X_val.shape, " y_tr:", y_tr.shape, " y_val:", y_val.shape)
                print("X_tr dtypes:\n", X_tr.dtypes)
                print("Sample X_tr head:\n", X_tr.head().to_dict())
                print("Sample y_tr unique:\n", pd.Series(y_tr).unique()[:20])
                import traceback
                traceback.print_exc()
                raise

        # Si todo ok, predecimos y calculamos AUC
        preds = model.predict_proba(X_val)[:, 1]
        oof_preds[val_idx] = preds
        auc = roc_auc_score(y_val, preds)
        val_scores.append(auc)
        models.append(model)
        print(f"fold {fold} auc: {auc:.4f} (tried: {tried_modes})")

    mean_auc = float(np.mean(val_scores)) if val_scores else 0.0
    return models, oof_preds, mean_auc





def main(args):
    set_seed()
    X, y = load_data(args.data_path, target_col=args.target_col)

    params = {
        "n_estimators": 10000,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "colsample_bytree": 0.8,
        "subsample": 0.8,
        "reg_alpha": 0.0,
        "reg_lambda": 1.0,
    }

    models, oof_preds, mean_auc = cross_val_train(X, y, params, n_splits=args.n_splits)
    print(f"OOF AUC: {mean_auc:.4f}")

    os.makedirs(args.output_dir, exist_ok=True)
    # Save one model (e.g. last fold) and OOF preds + metrics
    joblib.dump(models[-1], os.path.join(args.output_dir, "model_fold_last.joblib"))
    pd.DataFrame({"oof": oof_preds}).to_csv(os.path.join(args.output_dir, "oof_preds.csv"), index=False)
    with open(os.path.join(args.output_dir, "metrics.json"), "w") as f:
        json.dump({"oof_auc": mean_auc}, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--output-dir", type=str, default="artifacts/lightgbm")
    parser.add_argument("--n-splits", type=int, default=5)
    parser.add_argument("--target-col", type=str, default=None, help="Name of the target/label column in the dataset")
    args = parser.parse_args()
    main(args)
