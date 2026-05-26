# JWT Authentication API

Una aplicación Web API construida con Python y FastAPI que implementa autenticación JWT (JSON Web Token).

## Descripción

Esta API proporciona:
- **Endpoint de Login**: Autentica el usuario con usuario y contraseña, retorna un token JWT de acceso y un token de refresco
- **Endpoint de Refresco**: Permite refrescar el token de acceso usando el token de refresco
- **Endpoint de Salud**: Verifica el estado de la aplicación

## Características

- ✅ Autenticación JWT con HS256
- ✅ Token de acceso con expiración de 300 segundos
- ✅ Token de refresco con expiración de 7 días
- ✅ Validación de credenciales (usuario: admin, contraseña: admin123)
- ✅ Documentación automática con Swagger UI
- ✅ Contenedor Docker con docker-compose
- ✅ Gestión de dependencias con Poetry

## Requisitos

- Python 3.9+
- Poetry (para instalación local)
- Docker y Docker Compose (opcional, para despliegue en contenedores)

## Instalación Local

### 1. Instalar dependencias con Poetry

```bash
cd backend
poetry install
```

### 2. Crear archivo .env (opcional)

```bash
echo "SECRET_KEY=your-secret-key-change-this-in-production" > .env
```

### 3. Ejecutar la aplicación

```bash
poetry run python main.py
```

O usando uvicorn directamente:

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## Instalación con Docker

### 1. Construir y ejecutar con docker-compose

Desde la raíz del proyecto:

```bash
docker-compose up --build
```

La API estará disponible en: `http://localhost:8000`

### 2. Detener la aplicación

```bash
docker-compose down
```

## Uso de la API

### Documentación Interactiva

Acceda a la documentación interactiva de Swagger UI:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 1. Obtener Token (Login)

**Endpoint**: `POST /login`

**Request**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Ejemplo con curl**:
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 2. Refrescar Token

**Endpoint**: `POST /refresh`

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Ejemplo con curl**:
```bash
curl -X POST "http://localhost:8000/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

### 3. Verificar Salud de la Aplicación

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

**Ejemplo con curl**:
```bash
curl http://localhost:8000/health
```

## Estructura del Proyecto

```
backend/
├── main.py              # Aplicación FastAPI principal
├── config.py            # Configuración de la aplicación
├── models.py            # Modelos Pydantic para requests/responses
├── jwt_utils.py         # Funciones utilitarias para JWT
├── pyproject.toml       # Configuración de Poetry
├── Dockerfile           # Definición de imagen Docker
└── README.md            # Este archivo
```

## Configuración

Las siguientes variables de entorno pueden ser configuradas:

- `SECRET_KEY`: Clave secreta para firmar tokens JWT (default: "your-secret-key-change-this-in-production")
- `ALGORITHM`: Algoritmo para firmar JWT (default: "HS256")
- `ACCESS_TOKEN_EXPIRE_SECONDS`: Tiempo de expiración del token de acceso en segundos (default: 300)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Tiempo de expiración del token de refresco en días (default: 7)
- `HOST`: Host en el que escucha la aplicación (default: "0.0.0.0")
- `PORT`: Puerto en el que escucha la aplicación (default: 8000)

## Credenciales de Prueba

- **Usuario**: admin
- **Contraseña**: admin123

## Dependencias Principales

- **FastAPI**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI
- **python-jose**: Implementación de JWT
- **Passlib**: Hashing de contraseñas
- **Pydantic**: Validación de datos

## Testing

Para ejecutar pruebas (si están disponibles):

```bash
cd backend
poetry run pytest
```

## Seguridad

⚠️ **IMPORTANTE**: Para producción:
1. Cambiar `SECRET_KEY` por una clave segura y aleatoria
2. Usar HTTPS
3. Implementar validación contra una base de datos real
4. Añadir rate limiting
5. Implementar logging y monitoreo

## Licencia

Este proyecto está disponible bajo la licencia MIT.

## Autor

Desarrollado como ejercicio de implementación de JWT con FastAPI.
