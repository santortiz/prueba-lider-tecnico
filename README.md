# 🧾 Restaurant Reservation System – Backend

Este sistema permite gestionar reservas, mesas, salones y personal en un restaurante mediante una API RESTful desarrollada con FastAPI y una base de datos PostgreSQL. Incluye autenticación con JWT, envío de correos vía SendGrid y control de acceso por roles (admin, waiter).

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

## 🔐 Roles del sistema

- **admin**: Puede crear/eliminar personal, salones, mesas y reservas.
- **waiter**: Puede visualizar y gestionar reservas y ocupación de mesas, pero no realizar operaciones administrativas.

## 🧭 Estructura de endpoints

### 🔒 Auth (`/auth`)

| Método | Endpoint | Descripción                  |
| ------- | -------- | ----------------------------- |
| POST    | /login   | Login con email y contraseña |

### 🧑‍💼 Staff (`/staff`)

| Método | Endpoint | Rol requerido | Descripción                      |
| ------- | -------- | ------------- | --------------------------------- |
| POST    | /        | admin         | Crea un nuevo miembro del staff   |
| GET     | /        | cualquiera    | Lista todo el personal registrado |

### 🏨 Rooms (`/rooms`)

| Método | Endpoint | Rol requerido | Descripción             |
| ------- | -------- | ------------- | ------------------------ |
| POST    | /        | admin         | Crea un salón           |
| GET     | /        | cualquiera    | Lista todos los salones  |
| GET     | /{id}    | cualquiera    | Obtiene un salón por ID |
| DELETE  | /{id}    | admin         | Elimina un salón por ID |

### 🍽️ Tables (`/tables`)

| Método | Endpoint           | Rol requerido | Descripción                           |
| ------- | ------------------ | ------------- | -------------------------------------- |
| POST    | /                  | admin         | Crea una mesa                          |
| GET     | /                  | cualquiera    | Lista todas las mesas                  |
| GET     | /available-by-room | cualquiera    | Mesas disponibles agrupadas por salón |
| GET     | /{id}              | cualquiera    | Detalle de una mesa                    |
| DELETE  | /{id}              | admin         | Elimina una mesa                       |
| POST    | /{id}/occupy       | cualquiera    | Marca una mesa como ocupada (walk-in)  |
| POST    | /{id}/free         | cualquiera    | Marca una mesa como libre              |

### 📅 Reservations (`/reservations`)

| Método | Endpoint     | Rol requerido | Descripción                  |
| ------- | ------------ | ------------- | ----------------------------- |
| POST    | /            | admin         | Crea una reserva automática  |
| GET     | /            | cualquiera    | Lista todas las reservas      |
| GET     | /{id}        | cualquiera    | Detalle de una reserva        |
| DELETE  | /{id}        | admin         | Elimina una reserva           |
| POST    | /{id}/arrive | cualquiera    | Marca reserva como ocupada    |
| POST    | /{id}/finish | cualquiera    | Marca reserva como finalizada |

### 🧪 Healthcheck (`/health`)

| Método | Endpoint | Descripción                   |
| ------- | -------- | ------------------------------ |
| GET     | /health  | Verifica que la API esté viva |

## 🔄 Ciclo de vida de una reserva

1. **Creación**

   - Si `guests <= 6` y no se especifica `table_id`, el sistema asigna automáticamente la mejor mesa disponible.
   - Si `guests > 6`, se debe especificar `table_id`. La lista de mesas disponibles por salón puede obtenerse desde `/tables/available-by-room`.
2. **Llegada del cliente**

   - Se marca la reserva como `occupied` y la mesa asociada también.
3. **Finalización**

   - La reserva pasa a `finished` y la mesa vuelve a estar `free`.

### ⚠️ Conflictos con Walk-ins

Antes de permitir la ocupación de una mesa manualmente:

- Debe estar `free`
- No debe haber reservas en la hora actual o siguiente.

## 📧 Notificaciones por correo

Utiliza SendGrid con plantillas dinámicas. Se requiere:

```
SENDGRID_API_KEY=<tu_clave_api>
FROM_EMAIL=<correo_emisor>
TEMPLATE_ID=<id_plantilla>
```

## 🔐 Autenticación y autorización

- Basada en JWT.
- Roles definidos en el token (`admin`, `waiter`).
- Protección de rutas con `Depends(require_role(...))`.

## 🧪 Validaciones y normalización

- La hora de la reserva se trunca automáticamente a la hora cerrada (`HH:00`) en el backend.

## 📂 Estructura de carpetas

```
app/
├── main.py                 # Punto de entrada de la API
├── config.py               # Configuración vía variables de entorno
├── database.py             # Configuración y creación de la BD
├── models/                 # Modelos SQLAlchemy
├── routers/                # Rutas agrupadas
├── schemas/                # Esquemas Pydantic
├── services/               # Lógica de negocio
├── utils/                  # Utilidades (auth, email)
```

## 🚀 Despliegue local con Docker

### 🧱 Requisitos

- Docker
- Docker Compose

### 📝 Variables de entorno

Archivo `.env` al nivel del proyecto:

```
POSTGRES_DB=restaurant
POSTGRES_USER=admin
POSTGRES_PASSWORD=adminpassword
DATABASE_URL=postgresql+psycopg2://admin:adminpassword@db:5432/restaurant
FROM_EMAIL=your@email.com
SENDGRID_API_KEY=your_sendgrid_api_key
TEMPLATE_ID=your_template_id
JWT_SECRET=supersecretkey
```

### ▶️ Ejecutar el proyecto

```bash
docker compose -f docker/docker-compose.dev.yml up --build
```

### 📄 Acceso a la documentación

http://localhost:8000/docs

### 🛑 Detener los servicios

```bash
docker compose down
```

---

## 🧠 Justificación Tecnológica

### Backend – FastAPI + SQLAlchemy + PostgreSQL

#### ✅ ¿Por qué FastAPI?

- Moderno, rápido, y compatible con async/await.
- Validación y documentación automática con OpenAPI.
- Integración natural con Pydantic.
- Ideal para construir prototipos y soluciones productivas rápidamente.

#### ✅ ¿Por qué SQLAlchemy?

- ORM maduro, flexible y ampliamente utilizado.
- Soporte para relaciones complejas y acceso a SQL si es necesario.
- Integración directa con FastAPI y patrones de inyección de dependencias.

#### ✅ ¿Por qué PostgreSQL?

- Motor relacional robusto, confiable y ampliamente adoptado.
- Compatible con Docker, escalable, y con excelente soporte para integraciones modernas.

### Autenticación y Seguridad

- JWT con OAuth2.
- bcrypt para protección de contraseñas.
- Autorización basada en roles (`admin`, `waiter`).

### Notificaciones – SendGrid

- API profesional para envíos de correo.
- Soporta plantillas dinámicas.
- Escalable para producción.

### Modularidad

- Proyecto modular con separación clara por capas.
- Facilita mantenimiento, pruebas y escalabilidad.

## 🧠 Asignación Óptima de Mesas

El sistema incorpora un modelo de optimización matemática para asignar automáticamente reservas a mesas disponibles de forma eficiente. Esto es especialmente útil cuando múltiples reservas se registran sin una mesa específica y se desea maximizar la ocupación del restaurante minimizando desperdicio de espacio.

### 🎯 Objetivo

Asignar reservas del `pool` a las mesas disponibles de tal manera que:

- Cada reserva se asigna a una única mesa.
- Cada mesa se usa como máximo una vez.
- Solo se usan mesas cuya capacidad sea suficiente para los comensales de la reserva.
- **Se minimiza la cantidad total de sillas sin ocupar y la cantidad de reservas sin asignar**

### 📊 Formulación del modelo de optimización

Dado un conjunto de **reservas pendientes** y un conjunto de **mesas disponibles**, el sistema ejecuta un modelo de optimización que **asigna mesas minimizando la cantidad de sillas vacías y penalizando las reservas sin asignar**.

#### Conjuntos y parámetros

- \( R = \{r_1, r_2, \ldots, r_n\} \): Reservas, donde cada \( r_i \) tiene \( g_i \) comensales.
- \( T = \{t_1, t_2, \ldots, t_m\} \): Mesas, donde cada \( t_j \) tiene capacidad \( c_j \).
- \( x_{ij} \in \{0, 1\} \): Variable binaria, 1 si la reserva \( r_i \) se asigna a la mesa \( t_j \).
- \( y_i \in \{0, 1\} \): Variable binaria, 1 si la reserva \( r_i \) fue asignada a alguna mesa.
- \( \lambda \): Penalización por cada reserva no asignada.

#### Objetivo

Minimizar:

\[
\sum_{i=1}^{n} \sum_{j=1}^{m} x_{ij} \cdot (c_j - g_i) + \lambda \cdot \sum_{i=1}^{n} (1 - y_i)
\]

#### Restricciones

1. **Relación entre variables**: una reserva se marca como asignada si está asociada a alguna mesa

\[
\sum_{j=1}^{m} x_{ij} = y_i \quad \forall i \in R
\]

2. **Una mesa se asigna a lo sumo a una reserva**:

\[
\sum_{i=1}^{n} x_{ij} \leq 1 \quad \forall j \in T
\]

3. **Solo pueden asignarse mesas con capacidad suficiente**:

\[
x_{ij} = 0 \quad \text{si } g_i > c_j
\]

---

Este modelo permite encontrar una solución eficiente, asignando mesas de forma óptima incluso si algunas reservas no pueden ser satisfechas debido a limitaciones de capacidad o disponibilidad.

### ⚙️ Implementación

- El modelo está implementado en `app/utils/optimizer.py` utilizando `pulp`, una librería de optimización en Python.
- Se expone mediante el endpoint:

  ```
  POST /optimize?date=YYYY-MM-DD&time=HH:MM
  ```

- Este endpoint:
  - Consulta las reservas del `pool` para esa fecha y hora.
  - Consulta las mesas libres (es decir, que no tienen reservaciones asignadas).
  - Ejecuta el modelo de optimización.
  - Crea las reservas reales en la base de datos para las asignaciones exitosas.
  - Las reservas que no puedan ser asignadas (por conflicto u otra razón) se conservan en el `pool`.

### 📤 Ejemplo de respuesta

```json
{
  "assigned": [
    { "reservation_id": 1, "table_id": 12, "guests": 4, "capacity": 4 },
    { "reservation_id": 2, "table_id": 14, "guests": 2, "capacity": 2 }
  ],
  "unassigned": [
    { "reservation_id": 3, "table_id": 10, "guests": 6, "capacity": 6 }
  ]
}
```

Este enfoque mejora la eficiencia del restaurante al evitar dejar sillas vacías innecesariamente.