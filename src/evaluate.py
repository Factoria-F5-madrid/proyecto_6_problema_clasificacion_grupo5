# src/evaluate.py
import json
import pandas as pd
import argparse
from sklearn.metrics import roc_auc_score, log_loss

def main(args):
    oof = pd.read_csv(args.oof_path)["oof"].values
    y_true = pd.read_parquet(args.y_path)["target"].values

    auc = roc_auc_score(y_true, oof)
    ll = log_loss(y_true, oof)
    out = {"auc": float(auc), "log_loss": float(ll)}
    print(out)
    with open(args.out_json, "w") as f:
        json.dump(out, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--oof-path", required=True)
    parser.add_argument("--y-path", required=True)
    parser.add_argument("--out-json", default="artifacts/eval_metrics.json")
    args = parser.parse_args()
    main(args)
