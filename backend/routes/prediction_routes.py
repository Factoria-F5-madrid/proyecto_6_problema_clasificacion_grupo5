# backend/routes/prediction_routes.py
from fastapi import APIRouter
from backend.controllers.prediction_controller import router as prediction_router

router = APIRouter()
# mount controller routes at root of this router; main.py includes this under /api
router.include_router(prediction_router, prefix="", tags=["predict"])
