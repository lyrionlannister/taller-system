from datetime import datetime, timezone
from typing import Dict, List
from uuid import uuid4

from fastapi import HTTPException

from src.models.schemas import (
    AsignarOrdenRequest,
    CambiarEstadoRequest,
    CrearOrdenRequest,
    EstadoOrden,
    RegistrarDiagnosticoRequest,
    Rol,
)


class OrdenService:
    def __init__(self) -> None:
        self.clientes: Dict[str, dict] = {}
        self.vehiculos: Dict[str, dict] = {}
        self.ordenes: Dict[str, dict] = {}
        self.ordenes_by_id_rep: Dict[str, str] = {}
        self.diagnosticos: List[dict] = []
        self.eventos: List[dict] = []

        self.allowed_transitions = {
            EstadoOrden.CREADA: {EstadoOrden.ASIGNADA, EstadoOrden.CANCELADA},
            EstadoOrden.ASIGNADA: {EstadoOrden.EN_DIAGNOSTICO, EstadoOrden.CANCELADA},
            EstadoOrden.EN_DIAGNOSTICO: {EstadoOrden.EN_REPARACION, EstadoOrden.CANCELADA},
            EstadoOrden.EN_REPARACION: {EstadoOrden.LISTA_ENTREGA, EstadoOrden.CANCELADA},
            EstadoOrden.LISTA_ENTREGA: {EstadoOrden.ENTREGADA},
            EstadoOrden.ENTREGADA: set(),
            EstadoOrden.CANCELADA: set(),
        }

    def _generar_id_reparacion(self) -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        serial = len(self.ordenes) + 1
        return f"REP-{stamp}-{serial:04d}"

    def _emitir_evento(self, nombre: str, payload: dict) -> None:
        self.eventos.append(
            {
                "evento": nombre,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "payload": payload,
            }
        )

    def crear_orden(self, body: CrearOrdenRequest) -> dict:
        if body.actor_rol not in {Rol.ADMINISTRADOR, Rol.ASISTENTE}:
            raise HTTPException(status_code=403, detail="Solo ADMINISTRADOR o ASISTENTE pueden crear órdenes")

        cliente_id = str(uuid4())
        vehiculo_id = str(uuid4())
        orden_id = str(uuid4())
        id_reparacion = self._generar_id_reparacion()

        self.clientes[cliente_id] = {"id": cliente_id, **body.cliente.model_dump()}
        self.vehiculos[vehiculo_id] = {"id": vehiculo_id, "cliente_id": cliente_id, **body.vehiculo.model_dump()}

        orden = {
            "id": orden_id,
            "id_reparacion": id_reparacion,
            "cliente_id": cliente_id,
            "vehiculo_id": vehiculo_id,
            "descripcion_falla": body.descripcion_falla,
            "estado": EstadoOrden.CREADA,
            "estado_pago": body.estado_pago,
            "mecanico_id": None,
            "creado_en": datetime.now(timezone.utc).isoformat(),
        }
        self.ordenes[orden_id] = orden
        self.ordenes_by_id_rep[id_reparacion] = orden_id
        self._emitir_evento("orden_creada", {"id_reparacion": id_reparacion, "estado": orden["estado"]})
        return orden

    def asignar_orden(self, id_reparacion: str, body: AsignarOrdenRequest) -> dict:
        if body.actor_rol not in {Rol.ADMINISTRADOR, Rol.ASISTENTE}:
            raise HTTPException(status_code=403, detail="Solo ADMINISTRADOR o ASISTENTE pueden asignar")
        orden_id = self.ordenes_by_id_rep.get(id_reparacion)
        if not orden_id:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        orden = self.ordenes[orden_id]
        if orden["estado"] not in {EstadoOrden.CREADA, EstadoOrden.ASIGNADA}:
            raise HTTPException(status_code=409, detail="Orden no asignable en el estado actual")
        orden["mecanico_id"] = body.mecanico_id
        orden["estado"] = EstadoOrden.ASIGNADA
        self._emitir_evento("orden_asignada", {"id_reparacion": id_reparacion, "mecanico_id": body.mecanico_id})
        return orden

    def listar_ordenes_mecanico(self, mecanico_id: str) -> list:
        return [o for o in self.ordenes.values() if o["mecanico_id"] == mecanico_id]

    def cambiar_estado(self, id_reparacion: str, body: CambiarEstadoRequest) -> dict:
        if body.actor_rol not in {Rol.ADMINISTRADOR, Rol.MECANICO}:
            raise HTTPException(status_code=403, detail="Solo ADMINISTRADOR o MECANICO pueden cambiar estado")
        orden_id = self.ordenes_by_id_rep.get(id_reparacion)
        if not orden_id:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        orden = self.ordenes[orden_id]
        actual = orden["estado"]
        if body.nuevo_estado not in self.allowed_transitions[actual]:
            raise HTTPException(status_code=409, detail=f"Transición inválida: {actual} -> {body.nuevo_estado}")
        orden["estado"] = body.nuevo_estado
        self._emitir_evento("orden_estado_actualizado", {"id_reparacion": id_reparacion, "estado": body.nuevo_estado})
        return orden

    def registrar_diagnostico(self, id_reparacion: str, body: RegistrarDiagnosticoRequest) -> dict:
        if body.actor_rol != Rol.MECANICO:
            raise HTTPException(status_code=403, detail="Solo MECANICO puede registrar diagnóstico")
        orden_id = self.ordenes_by_id_rep.get(id_reparacion)
        if not orden_id:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        orden = self.ordenes[orden_id]
        if orden["mecanico_id"] != body.mecanico_id:
            raise HTTPException(status_code=403, detail="Mecánico no asignado a esta orden")

        registro = {
            "id": str(uuid4()),
            "orden_id": orden_id,
            "mecanico_id": body.mecanico_id,
            "resultado": body.resultado,
            "recomendacion_autoparte": body.recomendacion_autoparte,
            "notificar_cliente": body.notificar_cliente,
            "creado_en": datetime.now(timezone.utc).isoformat(),
        }
        self.diagnosticos.append(registro)
        self._emitir_evento(
            "diagnostico_registrado",
            {"id_reparacion": id_reparacion, "mecanico_id": body.mecanico_id, "notificar_cliente": body.notificar_cliente},
        )
        return registro

    def listar_eventos(self) -> list:
        return self.eventos
