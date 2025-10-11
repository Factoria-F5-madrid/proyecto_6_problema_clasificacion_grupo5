# backend/main.py
import os
import pickle
import traceback
from pathlib import Path
import joblib
import asyncio
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar tus rutas y DB init
from backend.routes.prediction_routes import router as prediction_routes
from backend.init_db import init_db as run_init_db

# Cargar .env si existe (busca en árbol)
env_path = find_dotenv()
if env_path:
    load_dotenv(env_path)

APP_TITLE = "Airline Passenger Satisfaction API"


def create_app() -> FastAPI:
    app = FastAPI(title=APP_TITLE, version="0.1.0")

    # Middleware CORS (permite probar con Postman o frontend local)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En producción limita a tus dominios
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Incluir las rutas bajo /api
    app.include_router(prediction_routes, prefix="/api")

    return app


app = create_app()


@app.on_event("startup")
async def on_startup():
    """
    1) Inicializar la base de datos (crear tablas en dev).
    2) Intentar cargar el modelo ML: joblib first, pickle fallback.
    """
    # 1️⃣ Inicializar la base de datos
    try:
        await run_init_db()
        print("✅ Base de datos inicializada correctamente.")
    except Exception as e:
        print("❌ Error al inicializar la base de datos:", e)
        traceback.print_exc()

    # 2️⃣ Cargar el modelo de Machine Learning (joblib -> pickle)
    try:
        # Calcular ruta por defecto relativa al project-root/models/...
        backend_dir = Path(__file__).resolve().parent  # backend/
        project_root = backend_dir.parent
        default_pkl = project_root / "models" / "decision_tree_model.pkl"
        default_joblib = project_root / "models" / "decision_tree_model.joblib"
        default_joblib_alt = project_root / "models" / "decision_tree_model.joblib.pkl"

        # Allow overriding via env var MODEL_PATH (absolute or relative to project root)
        env_path = os.getenv("MODEL_PATH")
        if env_path:
            candidate = Path(env_path)
            if not candidate.is_absolute():
                candidate = (project_root / candidate).resolve()
            model_path = candidate
        else:
            # Prefer explicit joblib file if present, else .pkl default
            if default_joblib.exists():
                model_path = default_joblib
            elif default_joblib_alt.exists():
                model_path = default_joblib_alt
            else:
                model_path = default_pkl

        model_path = model_path.resolve()

        if not model_path.exists():
            app.state.model = None
            app.state.model_version = None
            print(f"⚠️ No model found at {model_path}. Put your model in project_root/models/ and set MODEL_PATH if needed.")
            return

        # Try joblib first
        loaded = None
        joblib_exc = None
        pickle_exc = None

        try:
            loaded = joblib.load(model_path)
            print(f"✅ Model loaded with joblib from: {model_path}")
        except Exception as je:
            joblib_exc = traceback.format_exc()
            print("⚠️ joblib.load failed. Will try pickle as fallback.")
            # print short message
            print("joblib error:", je)

        # If joblib failed, try pickle
        if loaded is None:
            try:
                with open(model_path, "rb") as f:
                    loaded = pickle.load(f)
                print(f"✅ Model loaded with pickle from: {model_path}")
            except Exception as pe:
                pickle_exc = traceback.format_exc()
                print("❌ pickle.load also failed.")
                print("pickle error:", pe)

        # If neither worked, log full tracebacks
        if loaded is None:
            app.state.model = None
            app.state.model_version = None
            print("❌ Failed to load model with both joblib and pickle. Detailed errors:")
            if joblib_exc:
                print("==== joblib traceback ====")
                print(joblib_exc)
            if pickle_exc:
                print("==== pickle traceback ====")
                print(pickle_exc)
            return

        # Success
        app.state.model = loaded
        app.state.model_version = os.getenv("MODEL_VERSION", "v1")
        print(f"✅ Model is available in app.state (version={app.state.model_version}).")

    except Exception as e:
        app.state.model = None
        app.state.model_version = None
        print("❌ Unexpected error while loading model:", e)
        traceback.print_exc()


@app.on_event("shutdown")
async def on_shutdown():
    print("🛑 Cerrando la aplicación...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
