# Lite Thinking - Sistema de Gestión Empresarial

Prueba Técnica 2025 - Desarrollador Python, Django, React

## Tecnologías Utilizadas

### Backend
- **Python 3.11+**
- **Django 5.0** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos
- **JWT (SimpleJWT)** - Autenticación
- **ReportLab** - Generación de PDFs
- **drf-yasg** - Documentación Swagger

### Frontend
- **React 18** - Framework UI
- **Material-UI (MUI)** - Componentes UI
- **React Router 6** - Enrutamiento
- **Formik + Yup** - Formularios y validación
- **Atomic Design** - Arquitectura de componentes

### Funcionalidades Adicionales
- **Blockchain** - Verificación de integridad con hash SHA-256
- **Chatbot IA** - Integración con webhook n8n

## Estructura del Proyecto

```
prueba-tecnica/
├── backend/
│   ├── config/              # Configuración Django
│   ├── apps/
│   │   ├── users/           # Usuarios y autenticación
│   │   ├── empresas/        # Gestión de empresas
│   │   ├── productos/       # Catálogo de productos
│   │   ├── inventario/      # Control de inventario
│   │   ├── blockchain/      # Registro blockchain
│   │   └── chatbot/         # Chatbot IA
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    └── src/
        ├── components/
        │   ├── atoms/       # Componentes básicos
        │   ├── molecules/   # Combinación de atoms
        │   └── organisms/   # Componentes complejos
        ├── pages/           # Páginas
        ├── layouts/         # Layouts
        ├── api/             # Servicios API
        ├── context/         # Context API
        ├── hooks/           # Custom hooks
        └── routes/          # Rutas
```

## Instalación

### Requisitos Previos
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### 1. Configurar Base de Datos PostgreSQL

```sql
CREATE DATABASE litethinking_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE litethinking_db TO postgres;
```

### 2. Backend (Django)

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
copy .env.example .env
# Editar .env con tus credenciales

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

El backend estará disponible en: http://localhost:8000

### 3. Frontend (React)

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm start
```

El frontend estará disponible en: http://localhost:3000

## Endpoints API

### Autenticación
- `POST /api/auth/login/` - Iniciar sesión (retorna JWT)
- `POST /api/auth/register/` - Registrar usuario
- `GET /api/auth/me/` - Obtener usuario actual

### Empresas
- `GET /api/empresas/` - Listar empresas
- `POST /api/empresas/` - Crear empresa (admin)
- `GET /api/empresas/{nit}/` - Detalle empresa
- `PUT /api/empresas/{nit}/` - Actualizar (admin)
- `DELETE /api/empresas/{nit}/` - Eliminar (admin)

### Productos
- `GET /api/productos/` - Listar productos
- `POST /api/productos/` - Crear producto (admin)
- `GET /api/productos/{id}/` - Detalle producto
- `GET /api/productos/por_empresa/?nit=xxx` - Por empresa

### Inventario
- `GET /api/inventario/` - Listar inventario
- `POST /api/inventario/` - Crear item (admin)
- `GET /api/inventario/descargar-pdf/` - Descargar PDF
- `POST /api/inventario/enviar-pdf/` - Enviar por email

### Blockchain
- `GET /api/blockchain/` - Listar registros
- `GET /api/blockchain/verificar/` - Verificar integridad
- `GET /api/blockchain/estadisticas/` - Estadísticas

### Chatbot
- `POST /api/chatbot/` - Enviar mensaje
- `GET /api/chatbot/historial/{session_id}/` - Historial

## Documentación API

- Swagger UI: http://localhost:8000/docs/
- ReDoc: http://localhost:8000/redocs/

## Roles de Usuario

### Administrador
- CRUD completo de empresas
- CRUD completo de productos
- Gestión de inventario
- Envío de PDFs por email
- Gestión de usuarios

### Externo
- Visualización de empresas (solo lectura)
- Visualización de productos
- Descarga de PDFs
- Acceso al chatbot

## Funcionalidades Implementadas

### Requerimientos Base
- [x] Vista Empresa (NIT, nombre, dirección, teléfono)
- [x] Vista Productos (código, nombre, características, precios múltiples monedas)
- [x] Vista Login (correo, contraseña encriptada)
- [x] Vista Inventario (PDF, envío por email)
- [x] Roles: Administrador y Externo
- [x] Contraseñas encriptadas (Django hash)

### Funcionalidades Adicionales
- [x] **Blockchain**: Registro inmutable de transacciones con hash SHA-256
- [x] **Chatbot IA**: Integración con webhook n8n para asistente virtual
- [x] **Atomic Design**: Arquitectura de componentes (Atoms, Molecules, Organisms)

## Configuración del Chatbot

El chatbot se conecta al webhook de n8n configurado en:
```
CHATBOT_WEBHOOK_URL=http://localhost:5678/webhook/emily-tech-chatbot
```

## Variables de Entorno

### Backend (.env)
```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
DB_NAME=litethinking_db
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
CHATBOT_WEBHOOK_URL=http://localhost:5678/webhook/emily-tech-chatbot
```

## Licencia

Proyecto desarrollado para prueba técnica Lite Thinking 2025.
