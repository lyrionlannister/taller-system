from fastapi import FastAPI

from src.controllers.orden_controller import OrdenController
from src.routes.orden_routes import build_orden_router
from src.services.orden_service import OrdenService

app = FastAPI(title="Taller System API", version="0.1.0")

orden_service = OrdenService()
orden_controller = OrdenController(orden_service)

app.include_router(build_orden_router(orden_controller))
