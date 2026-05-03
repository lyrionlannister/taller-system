from src.models.schemas import (
    AsignarOrdenRequest,
    CambiarEstadoRequest,
    CrearOrdenRequest,
    RegistrarDiagnosticoRequest,
)
from src.services.orden_service import OrdenService


class OrdenController:
    def __init__(self, service: OrdenService) -> None:
        self.service = service

    def crear_orden(self, body: CrearOrdenRequest):
        return self.service.crear_orden(body)

    def asignar_orden(self, id_reparacion: str, body: AsignarOrdenRequest):
        return self.service.asignar_orden(id_reparacion, body)

    def listar_ordenes_mecanico(self, mecanico_id: str):
        return self.service.listar_ordenes_mecanico(mecanico_id)

    def cambiar_estado(self, id_reparacion: str, body: CambiarEstadoRequest):
        return self.service.cambiar_estado(id_reparacion, body)

    def registrar_diagnostico(self, id_reparacion: str, body: RegistrarDiagnosticoRequest):
        return self.service.registrar_diagnostico(id_reparacion, body)

    def listar_eventos(self):
        return self.service.listar_eventos()
