# =============================================================================
# Dockerfile - Backend API
# Sistema de Inventario Lite Thinking
# Arquitectura Limpia con Poetry
# =============================================================================

FROM python:3.11-slim

# Metadata
LABEL maintainer="Lite Thinking"
LABEL description="Backend API - Sistema de Inventario con Arquitectura Limpia"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Agregar Poetry al PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instalar dependencias del sistema (incluye cairo para PDF)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Crear directorios de trabajo
WORKDIR /app

# =============================================================================
# ARQUITECTURA LIMPIA: El dominio se copia al contenedor
# El backend lo consume como paquete local via Poetry
# =============================================================================

# Copiar el paquete de dominio (se copia desde el contexto del docker-compose)
COPY domain/ /domain/

# Copiar archivos de configuracion de Poetry del backend
COPY backend/pyproject.toml backend/poetry.lock* ./

# Actualizar la ruta del dominio para el contenedor y regenerar lock
RUN sed -i 's|path = "../domain"|path = "/domain"|g' pyproject.toml && \
    poetry lock --no-update && \
    poetry install --only main --no-root

# Copiar codigo del backend
COPY backend/ .

# Crear directorios necesarios
RUN mkdir -p /app/staticfiles /app/media

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/swagger/ || exit 1

# Comando para iniciar (produccion usaria gunicorn)
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
