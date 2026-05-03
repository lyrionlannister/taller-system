from fastapi import APIRouter

from src.controllers.orden_controller import OrdenController
from src.models.schemas import (
    AsignarOrdenRequest,
    CambiarEstadoRequest,
    CrearOrdenRequest,
    RegistrarDiagnosticoRequest,
)


def build_orden_router(controller: OrdenController) -> APIRouter:
    router = APIRouter(prefix="/v1", tags=["Ordenes"])

    @router.post("/ordenes")
    def crear_orden(body: CrearOrdenRequest):
        return controller.crear_orden(body)

    @router.patch("/ordenes/{id_reparacion}/asignar")
    def asignar_orden(id_reparacion: str, body: AsignarOrdenRequest):
        return controller.asignar_orden(id_reparacion, body)

    @router.get("/mecanicos/{mecanico_id}/ordenes")
    def listar_ordenes_mecanico(mecanico_id: str):
        return controller.listar_ordenes_mecanico(mecanico_id)

    @router.patch("/ordenes/{id_reparacion}/estado")
    def cambiar_estado(id_reparacion: str, body: CambiarEstadoRequest):
        return controller.cambiar_estado(id_reparacion, body)

    @router.post("/ordenes/{id_reparacion}/diagnostico")
    def registrar_diagnostico(id_reparacion: str, body: RegistrarDiagnosticoRequest):
        return controller.registrar_diagnostico(id_reparacion, body)

    @router.get("/eventos")
    def listar_eventos():
        return controller.listar_eventos()

    return router
