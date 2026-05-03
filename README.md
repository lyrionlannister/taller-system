# r-repuestos-system

Monorepo para un sistema de venta de repuestos para vehiculos de manera automatica.

## Arquitectura

Este repositorio esta organizado como un monorepo y sigue una arquitectura de microservicios.

Los servicios se comunican a traves de eventos, lo que permite desacoplar responsabilidades, escalar componentes de forma independiente y facilitar la integracion entre modulos del sistema.

## Estructura del repositorio

Esta es la organizacion principal del monorepo y lo que debe contener cada carpeta.

### `apps/`

Contiene las aplicaciones y servicios principales del sistema.

- `apps/agents/`: Agentes de inteligencia artificial del sistema.
- `apps/api/`: servicios backend o puertas de entrada al sistema.
- `apps/client/`: interfaces de usuario o aplicaciones cliente.

Uso esperado:
Aqui viven los microservicios, aplicaciones de borde y procesos que forman parte del negocio.

### `infra/`

Contiene la configuracion y recursos de infraestructura necesarios para ejecutar el sistema.

- `infra/database/`: configuracion, recursos y soporte para la capa de datos.
- `infra/docker/`: contenedores, imagenes y definiciones de entorno.
- `infra/network/`: configuraciones de red y comunicacion entre servicios.

Uso esperado:
Esta carpeta debe usarse para todo lo relacionado con despliegue, soporte tecnico del entorno y dependencias de infraestructura.

### `packages/`

Carpeta reservada para paquetes compartidos del monorepo.

Uso esperado:
No debe ser usada, modificada ni poblada sin autorizacion previa. Cualquier incorporacion en esta carpeta debe ser validada antes de implementarse.

## Nota de trabajo

Antes de agregar nuevos modulos o servicios, mantener la separacion por responsabilidades y respetar la comunicacion basada en eventos entre microservicios.

## Docker

La orquestacion del entorno se divide en dos archivos dentro de `infra/docker`:

- `infraestructure.yaml`: Nginx, base de datos y Redis.
- `apps.yaml`: servicios de `apps/api`, `apps/mcp` y `apps/agents`.

La imagen y configuracion de `nginx` viven en `infra/nginx/`, porque hacen parte de la infraestructura del entorno aunque se ejecuten como contenedor.

El archivo raiz [`docker-compose.yaml`](c:\Users\luisg\Documents\my-repositories\r-respuestos-system\docker-compose.yaml) incluye ambos para levantar todo junto.

Todos los contenedores usan:

- el mismo archivo `.env`
- la misma red Docker
- `TZ=America/Bogota`

Variables compartidas importantes:

- `DATABASE_HOST`
- `DATABASE_PORT`
- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `DATABASE_NAME`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_USERNAME`
- `REDIS_PASSWORD`
- `OPENAI_API_KEY`
- `WHATSAPP_VERIFY_TOKEN`
- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_API_VERSION`

Para levantar todo:

```bash
podman compose --env-file .env up --build -d
```

## Postgres y pgAdmin

Postgres ya no debe exponerse directamente al host. La exposicion de `5432` queda a cargo de un proxy TCP con rate limit por IP, para frenar intentos repetidos de autenticacion sin romper el acceso administrativo.

Uso esperado:

- `apps/api` sigue conectando internamente a `postgres:5432`
- `pgAdmin` puede seguir conectando al mismo `host:5432`
- el proxy rechaza rafagas de conexiones nuevas desde la misma IP antes de que lleguen directo a Postgres

La configuracion del proxy vive en `infra/haproxy/haproxy.cfg`. Si `pgAdmin` alguna vez necesitara mas conexiones concurrentes o mas sesiones nuevas en una ventana corta, ahi mismo se ajustan los limites.

## SSL con Certbot

La emision de certificados se hace mejor en el host con `certbot` usando el plugin `webroot`, mientras `nginx` en el contenedor expone `/.well-known/acme-challenge/` mediante `deploy/certbot/www`.

Preparar el directorio:

```bash
mkdir -p deploy/certbot/www
```

Levantar la infraestructura:

```bash
podman compose --env-file .env up --build -d
```

Emitir el certificado para el subdominio del backend:

```bash
certbot certonly \
  --webroot \
  -w /root/my-repositories/r-repuestos-system/deploy/certbot/www \
  -d api.24-7rrepuestos.com.co
```

La documentacion oficial de Certbot recomienda `certonly --webroot` cuando ya tienes un servidor web sirviendo el challenge temporalmente.
