-- Sprint 1 - Base operativa para talleres mecánicos

create extension if not exists pgcrypto;

create table if not exists usuarios (
  id uuid primary key default gen_random_uuid(),
  nombre text not null,
  email text not null unique,
  rol text not null check (rol in ('ADMINISTRADOR','ASISTENTE','MECANICO')),
  activo boolean not null default true,
  creado_en timestamptz not null default now()
);

create table if not exists clientes (
  id uuid primary key default gen_random_uuid(),
  nombre text not null,
  telefono text,
  email text,
  creado_en timestamptz not null default now()
);

create table if not exists vehiculos (
  id uuid primary key default gen_random_uuid(),
  cliente_id uuid not null references clientes(id),
  placa text not null unique,
  marca text,
  modelo text,
  anio integer,
  creado_en timestamptz not null default now()
);

create table if not exists ordenes_reparacion (
  id uuid primary key default gen_random_uuid(),
  id_reparacion text not null unique,
  cliente_id uuid not null references clientes(id),
  vehiculo_id uuid not null references vehiculos(id),
  descripcion_falla text not null,
  estado text not null check (estado in ('CREADA','ASIGNADA','EN_DIAGNOSTICO','EN_REPARACION','LISTA_ENTREGA','ENTREGADA','CANCELADA')) default 'CREADA',
  estado_pago text not null check (estado_pago in ('PAGADO','PENDIENTE')) default 'PENDIENTE',
  mecanico_id uuid references usuarios(id),
  creado_por uuid not null references usuarios(id),
  actualizado_en timestamptz not null default now(),
  creado_en timestamptz not null default now()
);

create table if not exists auditoria_ordenes (
  id uuid primary key default gen_random_uuid(),
  orden_id uuid not null references ordenes_reparacion(id),
  actor_id uuid not null references usuarios(id),
  accion text not null,
  detalle jsonb not null default '{}'::jsonb,
  creado_en timestamptz not null default now()
);

create table if not exists diagnosticos (
  id uuid primary key default gen_random_uuid(),
  orden_id uuid not null references ordenes_reparacion(id),
  mecanico_id uuid not null references usuarios(id),
  resultado text not null,
  recomendacion_autoparte text,
  notificar_cliente boolean not null default false,
  creado_en timestamptz not null default now()
);

create index if not exists idx_ordenes_placa on vehiculos(placa);
create index if not exists idx_ordenes_estado on ordenes_reparacion(estado);
create index if not exists idx_ordenes_creado_en on ordenes_reparacion(creado_en);
create index if not exists idx_auditoria_orden on auditoria_ordenes(orden_id, creado_en);
