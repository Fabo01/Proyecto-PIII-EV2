# Guía de Despliegue y Configuración

## Descripción General
Esta guía proporciona instrucciones detalladas para el despliegue, configuración y administración del Sistema de Simulación Logística de Drones. Incluye configuraciones para desarrollo, testing y producción.

## 🚀 Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10/11, Ubuntu 18.04+, macOS 10.15+
- **Python**: 3.9 o superior
- **RAM**: 4GB mínimo (8GB recomendado)
- **Almacenamiento**: 2GB espacio libre
- **Red**: Acceso a internet para dependencias

### Requisitos Recomendados para Producción
- **CPU**: 4 cores o más
- **RAM**: 16GB o superior
- **Almacenamiento**: SSD con 10GB espacio libre
- **Red**: Conexión estable de banda ancha

## 📦 Instalación y Configuración

### 1. Preparación del Entorno

#### Clonar el Repositorio
```bash
git clone <repository-url>
cd Proyecto-PIII-EV2
```

#### Crear Entorno Virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalación de Dependencias

#### Dependencias del Backend
```bash
pip install -r requirements.txt
```

#### requirements.txt
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
streamlit==1.28.1
matplotlib==3.7.2
networkx==3.1
plotly==5.17.0
pandas==2.1.3
numpy==1.24.3
requests==2.31.0
pytest==7.4.3
pytest-cov==4.1.0
behave==1.2.6
```

#### Verificar Instalación
```bash
python -c "import fastapi, streamlit, matplotlib, networkx; print('Todas las dependencias instaladas correctamente')"
```

### 3. Configuración del Sistema

#### Variables de Entorno
Crear archivo `.env` en el directorio raíz:
```env
# Configuración del Backend
BACKEND_HOST=localhost
BACKEND_PORT=8000
DEBUG_MODE=true
LOG_LEVEL=INFO

# Configuración del Frontend
FRONTEND_HOST=localhost
FRONTEND_PORT=8501
API_BASE_URL=http://localhost:8000

# Configuración de la Simulación
MAX_VERTICES=150
MAX_ARISTAS=300
MAX_PEDIDOS=500
AUTONOMIA_DRON=50

# Configuración de Logging
LOG_DIR=logs
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5

# Configuración de Rendimiento
CACHE_SIZE=1000
POOL_SIZE=100
MAX_WORKERS=4
```

#### Estructura de Directorios
```
Proyecto-PIII-EV2/
├── Backend/                 # Lógica de negocio y API
├── frontend/               # Interfaz principal (deprecated)
├── frontendv2/            # Interfaz optimizada
├── Docs/                  # Documentación completa
├── logs/                  # Archivos de log (creado automáticamente)
├── tests/                 # Suite de pruebas
├── .env                   # Variables de entorno
├── requirements.txt       # Dependencias Python
├── docker-compose.yml     # Configuración Docker
└── README.md             # Documentación básica
```

## 🔧 Configuración Avanzada

### 1. Configuración de Logging

#### logging_config.py
```python
import logging
import logging.handlers
import os
from datetime import datetime

def configurar_logging(nivel=logging.INFO, directorio_logs="logs"):
    """Configurar sistema de logging centralizado"""
    
    # Crear directorio de logs si no existe
    os.makedirs(directorio_logs, exist_ok=True)
    
    # Configuración del formato
    formato = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Logger principal del sistema
    logger = logging.getLogger('simulacion_drones')
    logger.setLevel(nivel)
    
    # Handler para archivo rotativo
    archivo_log = os.path.join(directorio_logs, 'simulacion.log')
    file_handler = logging.handlers.RotatingFileHandler(
        archivo_log,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formato)
    file_handler.setLevel(nivel)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formato)
    console_handler.setLevel(nivel)
    
    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Configurar loggers específicos
def configurar_loggers_sistema():
    """Configurar loggers para diferentes componentes"""
    
    loggers_config = {
        'simulacion_drones.api': 'INFO',
        'simulacion_drones.dominio': 'DEBUG',
        'simulacion_drones.algoritmos': 'DEBUG',
        'simulacion_drones.rendimiento': 'INFO',
        'simulacion_drones.errores': 'ERROR'
    }
    
    for logger_name, level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, level))
```

### 2. Configuración de la Base de Datos (Futuro)

#### database_config.py
```python
# Configuración para migración futura a base de datos persistente

DATABASE_CONFIG = {
    'development': {
        'engine': 'sqlite',
        'path': 'simulacion_dev.db',
        'echo': True
    },
    'testing': {
        'engine': 'sqlite',
        'path': ':memory:',
        'echo': False
    },
    'production': {
        'engine': 'postgresql',
        'host': 'localhost',
        'port': 5432,
        'database': 'simulacion_drones',
        'username': 'simulacion_user',
        'password': 'secure_password'
    }
}

def obtener_config_db(entorno='development'):
    """Obtener configuración de base de datos según entorno"""
    return DATABASE_CONFIG.get(entorno, DATABASE_CONFIG['development'])
```

## 🐳 Despliegue con Docker

### 1. Dockerfile para Backend
```dockerfile
# Dockerfile.backend
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY Backend/ ./Backend/
COPY .env .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "Backend.API.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Dockerfile para Frontend
```dockerfile
# Dockerfile.frontend
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY frontendv2/ ./frontendv2/
COPY .env .

# Exponer puerto
EXPOSE 8501

# Comando de inicio
CMD ["streamlit", "run", "frontendv2/main.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

### 3. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG_MODE=false
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - API_BASE_URL=http://backend:8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend

volumes:
  logs:
```

### 4. Configuración Nginx
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }
    
    upstream frontend {
        server frontend:8501;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        # Redirigir HTTP a HTTPS en producción
        # return 301 https://$server_name$request_uri;
        
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location / {
            proxy_pass http://frontend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Configuración para WebSocket (Streamlit)
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
    
    # Configuración HTTPS para producción
    # server {
    #     listen 443 ssl;
    #     server_name localhost;
    #     
    #     ssl_certificate /etc/nginx/ssl/cert.pem;
    #     ssl_certificate_key /etc/nginx/ssl/key.pem;
    #     
    #     # Configuración SSL moderna
    #     ssl_protocols TLSv1.2 TLSv1.3;
    #     ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    #     ssl_prefer_server_ciphers off;
    #     
    #     # Resto de configuración igual que HTTP
    # }
}
```

## 🚀 Comandos de Despliegue

### Desarrollo Local
```bash
# Iniciar backend
uvicorn Backend.API.main:app --reload --host localhost --port 8000

# En otra terminal, iniciar frontend
streamlit run frontendv2/main.py --server.port 8501

# Verificar servicios
curl http://localhost:8000/health
curl http://localhost:8501/_stcore/health
```

### Docker Development
```bash
# Construir y ejecutar
docker-compose up --build

# Solo reconstruir servicios específicos
docker-compose up --build backend
docker-compose up --build frontend

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Parar servicios
docker-compose down
```

### Producción
```bash
# Configurar variables de entorno de producción
export DEBUG_MODE=false
export LOG_LEVEL=WARNING
export API_BASE_URL=https://your-domain.com/api

# Ejecutar con configuración de producción
docker-compose -f docker-compose.prod.yml up -d

# Monitorear logs
docker-compose logs -f --tail=100
```

## 🔍 Monitoreo y Mantenimiento

### 1. Health Checks

#### Backend Health Check
```python
# Backend/API/health.py
from fastapi import APIRouter
from pydantic import BaseModel
import psutil
import time

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    version: str
    memory_usage: float
    cpu_usage: float
    uptime: float

start_time = time.time()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de verificación de salud del sistema"""
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        version="1.0.0",
        memory_usage=psutil.virtual_memory().percent,
        cpu_usage=psutil.cpu_percent(),
        uptime=time.time() - start_time
    )

@router.get("/health/detailed")
async def detailed_health_check():
    """Verificación detallada de componentes"""
    checks = {
        "api": await check_api_health(),
        "memory": await check_memory_health(),
        "disk": await check_disk_health(),
        "dependencies": await check_dependencies_health()
    }
    
    overall_status = "healthy" if all(
        check["status"] == "healthy" for check in checks.values()
    ) else "unhealthy"
    
    return {
        "overall_status": overall_status,
        "checks": checks,
        "timestamp": time.time()
    }
```

### 2. Scripts de Monitoreo

#### monitor.sh
```bash
#!/bin/bash
# Script de monitoreo automático

LOG_DIR="logs"
HEALTH_LOG="$LOG_DIR/health_check.log"

# Crear directorio de logs si no existe
mkdir -p $LOG_DIR

check_service() {
    local service_name=$1
    local url=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if curl -s --max-time 10 "$url" > /dev/null; then
        echo "[$timestamp] $service_name: OK" >> $HEALTH_LOG
        return 0
    else
        echo "[$timestamp] $service_name: FAILED" >> $HEALTH_LOG
        return 1
    fi
}

# Verificar servicios
echo "Verificando servicios..."

if check_service "Backend" "http://localhost:8000/health"; then
    echo "✅ Backend está funcionando"
else
    echo "❌ Backend no responde"
    # Reintentar o alertar
fi

if check_service "Frontend" "http://localhost:8501/_stcore/health"; then
    echo "✅ Frontend está funcionando"
else
    echo "❌ Frontend no responde"
fi

# Verificar uso de recursos
memory_usage=$(free | awk 'FNR==2{printf "%.2f", $3/$2*100}')
disk_usage=$(df / | awk 'FNR==2{print $5}' | sed 's/%//')

echo "Uso de memoria: ${memory_usage}%"
echo "Uso de disco: ${disk_usage}%"

# Alertas si es necesario
if (( $(echo "$memory_usage > 80" | bc -l) )); then
    echo "⚠️  ADVERTENCIA: Uso de memoria alto: ${memory_usage}%"
fi

if [ "$disk_usage" -gt 80 ]; then
    echo "⚠️  ADVERTENCIA: Uso de disco alto: ${disk_usage}%"
fi
```

### 3. Rotación de Logs

#### logrotate.conf
```conf
/app/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    copytruncate
    maxage 30
}
```

## 🔐 Configuración de Seguridad

### 1. Variables de Entorno Seguras
```bash
# .env.production
DEBUG_MODE=false
LOG_LEVEL=WARNING
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ORIGINS=https://your-domain.com

# Base de datos (si se implementa)
DB_PASSWORD=very-secure-database-password
DB_SSL_MODE=require
```

### 2. Configuración CORS
```python
# Backend/API/main.py
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Configuración CORS para producción
if os.getenv("DEBUG_MODE", "true").lower() == "false":
    allowed_origins = os.getenv("CORS_ORIGINS", "").split(",")
else:
    allowed_origins = ["*"]  # Solo para desarrollo

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## 📊 Métricas de Despliegue

### 1. KPIs de Sistema
- **Disponibilidad**: > 99.5% uptime
- **Tiempo de respuesta**: < 2 segundos para operaciones principales
- **Throughput**: > 100 requests/segundo
- **Uso de memoria**: < 70% en operación normal
- **Uso de CPU**: < 60% en operación normal

### 2. Alertas Automáticas
```python
# monitoring/alerts.py
import smtplib
from email.mime.text import MIMEText

def enviar_alerta(tipo, mensaje, metrica_valor=None):
    """Enviar alerta por email o webhook"""
    
    if tipo == "CRITICO":
        # Enviar alerta inmediata
        enviar_email_alerta(f"🚨 CRÍTICO: {mensaje}")
        
    elif tipo == "ADVERTENCIA":
        # Log y posible notificación
        logger.warning(f"⚠️  {mensaje}")
        
    # Webhook a Slack/Discord si está configurado
    if os.getenv("WEBHOOK_URL"):
        enviar_webhook_alerta(tipo, mensaje)

def verificar_metricas():
    """Verificar métricas y disparar alertas si es necesario"""
    metricas = obtener_metricas_sistema()
    
    if metricas.get("memory_usage", 0) > 85:
        enviar_alerta("CRITICO", f"Uso de memoria: {metricas['memory_usage']}%")
    
    if metricas.get("response_time", 0) > 5000:  # 5 segundos
        enviar_alerta("ADVERTENCIA", f"Tiempo de respuesta alto: {metricas['response_time']}ms")
```

## 🔄 Procedimientos de Mantenimiento

### 1. Backup Automático
```bash
#!/bin/bash
# backup.sh - Script de respaldo automático

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/app"

# Crear directorio de backup
mkdir -p $BACKUP_DIR

# Backup de logs importantes
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" $APP_DIR/logs/

# Backup de configuración
cp $APP_DIR/.env "$BACKUP_DIR/config_$DATE.env"

# Limpiar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.env" -mtime +30 -delete

echo "Backup completado: $DATE"
```

### 2. Actualización del Sistema
```bash
#!/bin/bash
# update.sh - Script de actualización

echo "Iniciando actualización del sistema..."

# Backup antes de actualizar
./backup.sh

# Parar servicios
docker-compose down

# Actualizar código
git pull origin main

# Reconstruir imágenes
docker-compose build --no-cache

# Iniciar servicios
docker-compose up -d

# Verificar servicios
sleep 30
./monitor.sh

echo "Actualización completada"
```

Esta guía de despliegue proporciona una base sólida para implementar el sistema en diferentes entornos, desde desarrollo local hasta producción con alta disponibilidad.
