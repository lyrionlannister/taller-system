# Eventos para n8n (Sprint 1)

## Evento: orden_creada

Se emite al crear una orden de reparación.

Payload sugerido:

```json
{
  "evento": "orden_creada",
  "idReparacion": "REP-20260503-0001",
  "estado": "CREADA",
  "estadoPago": "PENDIENTE",
  "cliente": {
    "nombre": "Juan Perez",
    "telefono": "+57..."
  },
  "vehiculo": {
    "placa": "ABC123"
  },
  "timestamp": "2026-05-03T10:00:00Z"
}
```

## Evento: orden_asignada

Se emite cuando Asistente o Admin asigna un mecánico.

## Evento: diagnostico_registrado

Se emite cuando el mecánico registra diagnóstico y/o recomendación de autoparte.

## Reglas mínimas

- Reintentos: 3
- Timeout webhook: 5s
- Log de respuesta HTTP y cuerpo de error
- Idempotencia por `idReparacion + evento + timestamp`
