# 🧾 Restaurant Reservation System – Backend

Este sistema permite gestionar reservas, mesas, salones y personal en un restaurante mediante una API RESTful desarrollada con **FastAPI** y una base de datos **PostgreSQL**. Incluye autenticación con JWT, envío de correos vía SendGrid y control de acceso por roles (`admin`, `waiter`).

---

## 🛠 Tecnologías utilizadas

| Tecnología | Propósito                                       |
| ----------- | ------------------------------------------------ |
| FastAPI     | Framework principal para la API REST             |
| SQLAlchemy  | ORM para modelado y acceso a base de datos       |
| PostgreSQL  | Base de datos relacional                         |
| SendGrid    | Envío de correos electrónicos de confirmación |
| Pydantic    | Validación y serialización de datos            |
| JWT (PyJWT) | Autenticación y autorización                   |
| bcrypt      | Hashing seguro de contraseñas                   |
| Docker      | Contenedorización del entorno (opcional)        |

---

## 🔐 Roles del sistema

- `admin`: Puede crear/eliminar personal, salones, mesas y reservas.
- `waiter`: Puede visualizar y gestionar reservas y ocupación de mesas, pero no realizar operaciones administrativas.

---

## 🧭 Estructura de endpoints

### 🔒 Auth (`/auth`)

| Método | Endpoint   | Descripción                  |
| ------- | ---------- | ----------------------------- |
| POST    | `/login` | Login con email y contraseña |

### 🧑‍💼 Staff (`/staff`)

| Método | Endpoint | Rol requerido | Descripción                      |
| ------- | -------- | ------------- | --------------------------------- |
| POST    | `/`    | admin         | Crea un nuevo miembro del staff   |
| GET     | `/`    | cualquiera    | Lista todo el personal registrado |

### 🏨 Rooms (`/rooms`)

| Método | Endpoint       | Rol requerido | Descripción             |
| ------- | -------------- | ------------- | ------------------------ |
| POST    | `/`          | admin         | Crea un salón           |
| GET     | `/`          | cualquiera    | Lista todos los salones  |
| GET     | `/{room_id}` | cualquiera    | Obtiene un salón por ID |
| DELETE  | `/{room_id}` | admin         | Elimina un salón por ID |

### 🍽️ Tables (`/tables`)

| Método | Endpoint               | Rol requerido | Descripción                           |
| ------- | ---------------------- | ------------- | -------------------------------------- |
| POST    | `/`                  | admin         | Crea una mesa                          |
| GET     | `/`                  | cualquiera    | Lista todas las mesas                  |
| GET     | `/available-by-room` | cualquiera    | Mesas disponibles agrupadas por salón |
| GET     | `/{table_id}`        | cualquiera    | Detalle de una mesa                    |
| DELETE  | `/{table_id}`        | admin         | Elimina una mesa                       |
| POST    | `/{table_id}/occupy` | cualquiera    | Marca una mesa como ocupada (walk-in)  |
| POST    | `/{table_id}/free`   | cualquiera    | Marca una mesa como libre              |

### 📅 Reservations (`/reservations`)

| Método | Endpoint                     | Rol requerido | Descripción                  |
| ------- | ---------------------------- | ------------- | ----------------------------- |
| POST    | `/`                        | admin         | Crea una reserva automática  |
| GET     | `/`                        | cualquiera    | Lista todas las reservas      |
| GET     | `/{reservation_id}`        | cualquiera    | Detalle de una reserva        |
| DELETE  | `/{reservation_id}`        | admin         | Elimina una reserva           |
| POST    | `/{reservation_id}/arrive` | cualquiera    | Marca reserva como ocupada    |
| POST    | `/{reservation_id}/finish` | cualquiera    | Marca reserva como finalizada |

### 🧪 Healthcheck (`/health`)

| Método | Endpoint    | Descripción                   |
| ------- | ----------- | ------------------------------ |
| GET     | `/health` | Verifica que la API esté viva |

---

## 🔄 Ciclo de vida de una reserva

### 1. **Creación (POST `/reservations/`)**

- Cuando son menos de 6 personas y no se especifica `table_id`, el sistema buscará automáticamente la **mejor mesa disponible** (`capacity >= guests`, estado `free`, sin conflicto horario) y hará la asignación.
- Cuando más de 6 personas, es necesario especificar la table_id. La lista de tables disponibles por room para la fecha y el número de invitados se entrega por medio del endpoint (GET /tables/available-by-room).
- Se valida que no exista conflicto con otra reserva (`status != finished`).
- Se envía correo de confirmación si `notification_email` es provisto.

### 2. **Llegada del cliente (`/arrive`)**

- La reserva pasa de `reserved` a `occupied`.
- También se marca la mesa como `occupied`.

### 3. **Finalización (`/finish`)**

- La reserva pasa a `finished`.
- La mesa vuelve a estar `free`.

---

## ⚠️ Conflictos con Walk-ins

Los walk-ins (clientes sin reserva) ocupan mesas manualmente mediante `POST /tables/{id}/occupy`.Antes de permitir la ocupación:

- Se verifica que la mesa esté `free`.
- No debe haber una reserva existente en esa hora o la siguiente, con estado `reserved` o `occupied`.

Esto garantiza que no se asigne una mesa a un walk-in si hay una reserva próxima.

---

## 📧 Notificaciones por correo

Se usa **SendGrid** con plantillas dinámicas. Cuando se crea una reserva con `notification_email`, se envía una confirmación automática.

Variables de entorno necesarias:

```
SENDGRID_API_KEY=<tu_clave_api>
FROM_EMAIL=<correo_emisor>
TEMPLATE_ID=<id_plantilla>
```

---

## 🔐 Autenticación y autorización

- Autenticación basada en JWT.
- Roles definidos en el token: `admin`, `waiter`.
- Se usan `Depends(require_role(...))` para proteger endpoints según el rol.

---

## 🧪 Validaciones y normalización

- La hora de la reserva se **trunca automáticamente a la hora cerrada** (`HH:00`) en el backend para garantizar consistencia y evitar colisiones difíciles de controlar.

---

## 📂 Estructura de carpetas

```
app/
├── main.py                 # Punto de entrada de la API
├── config.py               # Configuración vía variables de entorno
├── database.py             # Configuración y creación de la BD
├── models/                 # Definición de modelos SQLAlchemy
├── routers/                # Definición de rutas agrupadas por entidad
├── schemas/                # Esquemas de entrada/salida Pydantic
├── services/               # Lógica de negocio por entidad
├── utils/                  # utilidades comunes (auth, email)
```

---

## 🚀 Despliegue local con Docker

### 🧱 Requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

### 📝 Variables de entorno

Crea un archivo `.env` en el directorio raíz del proyecto (al mismo nivel del `docker/` y `app/`) con el siguiente contenido (ajusta según tus credenciales):

```env
POSTGRES_DB=restaurant
POSTGRES_USER=admin
POSTGRES_PASSWORD=adminpassword
DATABASE_URL=postgresql+psycopg2://admin:adminpassword@db:5432/restaurant

FROM_EMAIL=your@email.com
SENDGRID_API_KEY=your_sendgrid_api_key
TEMPLATE_ID=your_template_id

JWT_SECRET=supersecretkey
```

---

### ▶️ Ejecutar el proyecto

Desde el directorio raiz, ejecuta:

```bash
docker compose -f docker/docker-compose.dev.yml up --build
```

Esto hará lo siguiente:

- Construirá la imagen del servicio FastAPI.
- Levantará un contenedor PostgreSQL.
- Expondrá la API en [`http://localhost:8000`](http://localhost:8000).
- Creará las tablas automáticamente al iniciar.

---

### 📄 Acceso a la documentación

Una vez levantado el entorno, puedes acceder a la documentación interactiva de la API en:

```
http://localhost:8000/docs
```

---

### 🛑 Detener los servicios

Para detener y eliminar los contenedores:

```bash
docker compose down
```

---

## 🧪 Tests

*No incluidos en esta versión inicial.*
