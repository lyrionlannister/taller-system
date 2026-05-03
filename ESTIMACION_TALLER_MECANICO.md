# Estimación y viabilidad: migrar a sistema de talleres mecánicos

## Resumen ejecutivo

Partiendo del estado actual del repositorio (base de monorepo y lineamientos, sin código funcional visible en esta rama), **la opción más viable es reutilizar la base de arquitectura y entorno, pero reconstruir los módulos de negocio** orientados al taller.

En términos prácticos: **no empezar 100% de cero**, pero sí hacer un **pivot fuerte de dominio**.

## Decisión recomendada

- **Reusar**:
  - estructura monorepo
  - convenciones de infraestructura (`infra/`, docker, base de datos, red)
  - enfoque de microservicios orientado a eventos
- **Reemplazar/retirar**:
  - frontend web de tienda (si existe en ramas activas)
  - módulo `agents`
  - catálogos/lógicas de venta de repuestos orientadas ecommerce
- **Crear nuevo dominio**:
  - flujo operativo de recepción, diagnóstico, asignación, reparación, entrega y cobro

## Alcance funcional solicitado

1. Roles:
   - Administrador
   - Asistente
   - Mecánico
   - Cliente (sin login)

2. Flujo principal:
   - Asistente registra cliente + vehículo + solicitud usando placa.
   - Se genera ID de reparación y estado de pago (pagado/pendiente).
   - Asistente asigna trabajo a mecánico.
   - Mecánico actualiza estado hasta “listo”.
   - Notificación al cliente al finalizar.

3. Módulos adicionales:
   - Registro de autopartes.
   - Registro de proveedores de autopartes.

4. Automatización:
   - Eliminar módulo de agentes.
   - Migrar automatizaciones a n8n.

5. Revisión técnica:
   - Se omite compatibilidad automática de partes.
   - Mecánico registra resultado técnico y sugerencias de cambio de producto.
   - Debe notificar a Asistente y Administrador.
   - Opción de notificar al cliente.

## Esfuerzo estimado (MVP)

> Supuesto: equipo de 2 desarrolladores fullstack + 1 QA parcial, con dedicación casi completa.

- **Fase 0: discovery y diseño funcional/técnico**: 3–5 días
- **Fase 1: base técnica (auth interna, RBAC, modelos, migraciones)**: 4–6 días
- **Fase 2: flujo de órdenes de reparación**: 6–9 días
- **Fase 3: asignación mecánicos y estados**: 3–4 días
- **Fase 4: revisión técnica + notificaciones internas/cliente**: 4–6 días
- **Fase 5: autopartes + proveedores (CRUD)**: 3–5 días
- **Fase 6: integración n8n (eventos, webhooks, plantillas)**: 4–7 días
- **Fase 7: pruebas integrales, hardening y despliegue**: 5–7 días

**Total MVP:** ~29 a 49 días hábiles (6 a 10 semanas).

## Comparación: reutilizar base vs empezar desde cero

### Opción A — Reutilizar base actual (recomendada)

**Pros**
- Menor tiempo de setup DevOps/infra.
- Reaprovecha estructura de servicios y convenciones.
- Reduce riesgo de errores iniciales de despliegue.

**Contras**
- Puede arrastrar decisiones del dominio anterior.
- Requiere limpieza de módulos no aplicables.

**Tiempo estimado:** 6–10 semanas.

### Opción B — Empezar de cero

**Pros**
- Diseño 100% limpio al dominio taller.
- Sin deuda del modelo ecommerce.

**Contras**
- Mayor tiempo en bootstrap técnico.
- Más riesgo en primera salida a producción.

**Tiempo estimado:** 8–12 semanas.

## Recomendación final

La alternativa más viable es **reusar la base técnica e infraestructura** y **reconstruir el dominio de negocio** de taller mecánico. Solo recomendaría empezar desde cero si en ramas activas existe una alta deuda técnica no corregible (por ejemplo, acoplamientos críticos, seguridad deficiente o despliegues inestables).

## Backlog sugerido (orden de implementación)

1. Modelo de datos del taller (clientes, vehículos, órdenes, estados, pagos, diagnósticos).
2. RBAC para Administrador/Asistente/Mecánico.
3. API de recepción por placa + generación de ID reparación.
4. Asignación de mecánico + transición de estados.
5. Registro de revisión técnica y recomendaciones.
6. Notificaciones internas (Admin/Asistente) + opcional cliente.
7. CRUD autopartes y proveedores.
8. Integración n8n (eventos: creada, asignada, observación técnica, lista, pago).
9. Eliminación definitiva del módulo de agentes.
10. Métricas operativas básicas (SLA por estado, tiempos de ciclo).
