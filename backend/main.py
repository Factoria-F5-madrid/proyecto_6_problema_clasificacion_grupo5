# backend/main.py
import os
import pickle
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import the route that aggregates the controller router
from routes.prediction_routes import router as prediction_routes
# import your init_db coroutine (archivo init_db.py en la raiz de backend)
from init_db import init_db as run_init_db

APP_TITLE = "Airline Passenger Satisfaction API"

def create_app() -> FastAPI:
    app = FastAPI(title=APP_TITLE, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ajustar a tu entorno
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include the routes under /api
    app.include_router(prediction_routes, prefix="/api")

    return app

app = create_app()

@app.on_event("startup")
async def on_startup():
    # 1) create tables (dev). init_db es la coroutine que tienes en init_db.py
    try:
        await run_init_db()
        print("DB inicializaada correctamente.")
    except Exception as e:
        print("DB inicializacion fallida:", e)

    # 2) load ML model into app.state
    model_path = os.getenv("MODEL_PATH", "models/airline_model_v1.pkl")
    try:
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                raw_model = pickle.load(f)
            app.state.model = raw_model
        else:
            app.state.model = None
            app.state.model_version = None
            print(f"No model found at {model_path}. Place your .joblib in that path.")
    except Exception as e:
        app.state.model = None
        app.state.model_version = None
        print("Error loading model:", e)

@app.on_event("shutdown")
async def on_shutdown():
    print("Shutting down app.")
