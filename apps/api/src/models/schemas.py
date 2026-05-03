from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Rol(str, Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    ASISTENTE = "ASISTENTE"
    MECANICO = "MECANICO"


class EstadoOrden(str, Enum):
    CREADA = "CREADA"
    ASIGNADA = "ASIGNADA"
    EN_DIAGNOSTICO = "EN_DIAGNOSTICO"
    EN_REPARACION = "EN_REPARACION"
    LISTA_ENTREGA = "LISTA_ENTREGA"
    ENTREGADA = "ENTREGADA"
    CANCELADA = "CANCELADA"


class EstadoPago(str, Enum):
    PAGADO = "PAGADO"
    PENDIENTE = "PENDIENTE"


class ClienteIn(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None


class VehiculoIn(BaseModel):
    placa: str = Field(min_length=3)
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None


class CrearOrdenRequest(BaseModel):
    actor_rol: Rol
    cliente: ClienteIn
    vehiculo: VehiculoIn
    descripcion_falla: str
    estado_pago: EstadoPago = EstadoPago.PENDIENTE


class AsignarOrdenRequest(BaseModel):
    actor_rol: Rol
    mecanico_id: str


class CambiarEstadoRequest(BaseModel):
    actor_rol: Rol
    nuevo_estado: EstadoOrden


class RegistrarDiagnosticoRequest(BaseModel):
    actor_rol: Rol
    mecanico_id: str
    resultado: str
    recomendacion_autoparte: Optional[str] = None
    notificar_cliente: bool = False
