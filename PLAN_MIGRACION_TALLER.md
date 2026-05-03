# Plan de migración total a sistema de talleres mecánicos

## Objetivo

Migrar completamente el sistema actual a un sistema operativo para talleres mecánicos, eliminando el enfoque de tienda y priorizando el flujo real de recepción, diagnóstico, reparación, notificación y entrega.

## Enfoque de ejecución

- Migración total por fases cortas.
- Entrega incremental con validación funcional semanal.
- Sin frontend cliente: operación interna por roles (Administrador, Asistente, Mecánico).
- Cliente sin login, con consulta/notificaciones por ID de reparación.

## Tareas globales (Work Breakdown Structure)

## 0) Gestión del proyecto

- [ ] Definir responsables por módulo (backend, DB, automatización, QA).
- [ ] Definir calendario de sprints (semanales o quincenales).
- [ ] Definir DoR/DoD por historia.
- [ ] Definir tablero y estados de trabajo.

## 1) Modelo de datos y dominio

- [ ] Diseñar entidades: `clientes`, `vehiculos`, `ordenes_reparacion`, `diagnosticos`, `asignaciones`, `pagos`, `notificaciones`, `autopartes`, `proveedores`.
- [ ] Definir estados de orden:
  - `CREADA`
  - `ASIGNADA`
  - `EN_DIAGNOSTICO`
  - `EN_REPARACION`
  - `LISTA_ENTREGA`
  - `ENTREGADA`
  - `CANCELADA`
- [ ] Definir reglas de negocio por transición de estado.
- [ ] Crear migraciones iniciales y constraints.
- [ ] Crear índices por `placa`, `id_reparacion`, `estado`, `fecha`.

## 2) Seguridad, autenticación y roles

- [ ] Implementar autenticación para usuarios internos.
- [ ] Crear RBAC:
  - `ADMINISTRADOR` (acceso total)
  - `ASISTENTE` (recepción, asignación, pagos, seguimiento)
  - `MECANICO` (diagnóstico, actualización técnica y estados)
- [ ] Restringir al cliente (sin login).
- [ ] Auditoría de acciones críticas (cambio de estado, reasignaciones, cobros).

## 3) Flujo operativo principal

- [ ] Endpoint/servicio para registrar cliente + vehículo + reparación usando placa.
- [ ] Generación de `ID_REPARACION` único.
- [ ] Registro de condición de pago (`PAGADO` / `PENDIENTE`).
- [ ] Asignación de orden a mecánico.
- [ ] Actualización de estado por mecánico.
- [ ] Cierre de orden y entrega.

## 4) Diagnóstico técnico y alertas internas

- [ ] Captura de revisión técnica por mecánico.
- [ ] Registro de recomendación de cambio de producto/autoparte.
- [ ] Notificación obligatoria a Asistente y Administrador.
- [ ] Opción de notificar al cliente.

## 5) Catálogo operativo

- [ ] CRUD de autopartes.
- [ ] CRUD de proveedores.
- [ ] Relación opcional autoparte-proveedor.
- [ ] Historial de costo/abastecimiento (si aplica en MVP+1).

## 6) Automatización con n8n

- [ ] Diseñar catálogo de eventos de negocio.
- [ ] Publicar eventos: orden creada, asignada, observación técnica, lista, pago.
- [ ] Integrar webhooks con n8n.
- [ ] Configurar flujos de notificación (interna/cliente).
- [ ] Definir reintentos y manejo de errores.

## 7) Eliminación de componentes anteriores

- [ ] Retirar módulo `agents` del stack.
- [ ] Retirar flujos y dependencias de ecommerce/tienda.
- [ ] Ajustar `docker compose` para arquitectura final.

## 8) QA, observabilidad y salida a producción

- [ ] Pruebas unitarias de reglas de estado.
- [ ] Pruebas de integración de flujo completo.
- [ ] Pruebas de permisos por rol.
- [ ] Pruebas de notificación y resiliencia n8n.
- [ ] Métricas mínimas: tiempo por etapa, órdenes abiertas, órdenes vencidas.
- [ ] Plan de despliegue y rollback.

---

## Inicio inmediato (Sprint 1) — “Base operativa”

### Entregables Sprint 1

- [ ] Modelo de datos inicial + migraciones base.
- [ ] Módulo de autenticación interna + RBAC.
- [ ] Caso de uso: crear orden de reparación por placa con ID único.
- [ ] Caso de uso: asignar mecánico y listar órdenes por estado.
- [ ] Evento `orden_creada` publicado para n8n.

### Historias de usuario Sprint 1

1. Como Asistente, quiero registrar cliente+vehículo+solicitud con placa para abrir una orden.
2. Como Asistente, quiero asignar una orden a un mecánico para iniciar el trabajo.
3. Como Mecánico, quiero ver mis órdenes asignadas para ejecutar la reparación.
4. Como Administrador, quiero ver todas las órdenes por estado para supervisar operación.

### Criterios de aceptación (mínimos)

- Se crea orden con `ID_REPARACION` único.
- La orden inicia en estado `CREADA`.
- Solo Asistente/Admin pueden asignar mecánico.
- Mecánico solo ve/actualiza órdenes asignadas.
- Se registra auditoría de creación y asignación.

## Riesgos y mitigaciones

- Riesgo: ambigüedad de flujo de negocio.
  - Mitigación: validación funcional semanal con stakeholders.
- Riesgo: retrasos por integración de notificaciones.
  - Mitigación: desacoplar por eventos + cola/reintentos en n8n.
- Riesgo: deuda heredada del sistema anterior.
  - Mitigación: eliminación explícita por fases y pruebas de regresión.

## Definición de listo para producción (MVP)

- Flujo completo desde recepción hasta entrega funcionando.
- Notificaciones internas activas en cambios críticos.
- Reporte básico operativo por estados y tiempos.
- RBAC aplicado y auditado.
- Integración n8n estable con reintentos.
