# Frontend Streamlit

Aplicación web en Streamlit con dos páginas:

- **Login** (`frontend/app.py`): autentica contra el backend (`POST /login`) y guarda `access_token` y `refresh_token` en `st.session_state`.
- **Bienvenida** (`frontend/pages/1_Bienvenida.py`): página protegida. Si no hay sesión activa, no permite el acceso y redirige al login.

## Requisitos

- Python 3.10+
- Backend ejecutándose (por defecto en `http://localhost:8000`)

## Instalación

```bash
cd frontend
python -m pip install -r requirements.txt
```

## Ejecución

```bash
cd frontend
streamlit run app.py
```

## Configuración

Variable opcional:

- `BACKEND_URL`: URL base del backend. Por defecto: `http://localhost:8000`

Ejemplo:

```bash
BACKEND_URL=http://localhost:8000 streamlit run app.py
```

## Credenciales de prueba

- Usuario: `admin`
- Contraseña: `admin123`

## Diseño

La interfaz aplica el estándar visual definido en `DESING.md` (archivo de diseño provisto en la raíz del proyecto, referido como `DESIGN.md` en el enunciado):

- paleta clara/oscura por secciones,
- color primario único `#0066cc` para acciones,
- botones tipo pill,
- tipografía de sistema con estilo cercano a SF Pro.
