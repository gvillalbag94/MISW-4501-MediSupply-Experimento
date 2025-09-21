# API Gateway con Flask

Un API Gateway robusto construido con Flask que actúa como punto de entrada único para todos los microservicios.

## 🚀 Características

- **Proxy HTTP**: Reenvía peticiones a los microservicios correspondientes
- **Autenticación**: Middleware de autenticación JWT
- **Rate Limiting**: Control de velocidad de peticiones
- **Logging**: Sistema de logging completo
- **Health Checks**: Monitoreo del estado de los servicios
- **CORS**: Soporte para Cross-Origin Resource Sharing
- **Configuración flexible**: Variables de entorno para configuración

## 📁 Estructura del Proyecto

```
gateway/
├── app.py                 # Versión simple del gateway
├── app_advanced.py        # Versión avanzada con middleware
├── run.py                 # Script de inicio
├── .env                   # Variables de entorno
├── Pipfile               # Dependencias de Python
├── config/
│   ├── __init__.py
│   └── settings.py       # Configuración del gateway
├── middleware/
│   ├── __init__.py
│   └── auth_middleware.py # Middleware de autenticación
└── utils/
    ├── __init__.py
    └── rate_limiter.py   # Rate limiting
```

## 🛠️ Instalación

1. **Instalar dependencias**:
   ```bash
   pipenv install
   ```

2. **Configurar variables de entorno**:
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

3. **Ejecutar el gateway**:
   ```bash
   # Modo simple
   python run.py --mode simple --port 5000
   
   # Modo avanzado (recomendado)
   python run.py --mode advanced --port 5000 --debug
   ```

## 🔧 Configuración

### Variables de Entorno

```env
# Configuración del servidor
GATEWAY_PORT=5000
FLASK_DEBUG=True
HOST=0.0.0.0

# URLs de los servicios
AUTENTICADOR_URL=http://localhost:6001
AUTORIZADOR_URL=http://localhost:6002
PRODUCTOS_URL=http://localhost:6003
PROVEDORES_URL=http://localhost:5004

# Configuración de logging
LOG_LEVEL=INFO

# Configuración de seguridad
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Rate limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# CORS
CORS_ORIGINS=*
```

## 📡 Endpoints

### Gateway Endpoints

- `GET /health` - Estado del gateway
- `GET /services` - Lista de servicios disponibles
- `GET /status` - Estado de todos los servicios
- `GET /me` - Información del usuario autenticado

### Proxy Endpoints

- `* /auth/*` - Proxy al servicio de autenticación
- `* /authz/*` - Proxy al servicio de autorización (requiere auth)
- `* /products/*` - Proxy al servicio de productos (requiere auth)
- `* /providers/*` - Proxy al servicio de proveedores (requiere auth)

## 🔐 Autenticación

El gateway soporta autenticación JWT. Para acceder a endpoints protegidos:

```bash
curl -H "Authorization: Bearer <token>" http://localhost:5000/products/
```

## 📊 Monitoreo

### Health Check
```bash
curl http://localhost:5000/health
```

### Estado de Servicios
```bash
curl http://localhost:5000/status
```

## 🚦 Rate Limiting

El gateway incluye rate limiting configurable:
- **Límite por defecto**: 100 requests por hora por IP
- **Configurable**: Via variables de entorno
- **Headers de respuesta**: Incluye información de límites

## 📝 Logging

El sistema de logging incluye:
- **Request/Response logging**: Todas las peticiones son registradas
- **Error logging**: Errores detallados con stack traces
- **Performance logging**: Tiempos de respuesta de servicios

## 🔄 Uso con Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install pipenv
RUN pipenv install --deploy

EXPOSE 5000

CMD ["pipenv", "run", "python", "run.py", "--mode", "advanced"]
```

## 🧪 Testing

```bash
# Test de salud
curl http://localhost:5000/health

# Test de servicios
curl http://localhost:5000/services

# Test de proxy (requiere servicio backend)
curl http://localhost:5000/auth/login
```

## 🚀 Producción

Para producción, usar Gunicorn:

```bash
pipenv install gunicorn
pipenv run gunicorn -w 4 -b 0.0.0.0:5000 app_advanced:app
```

## 📋 Dependencias

- **Flask**: Framework web
- **Flask-CORS**: Soporte CORS
- **requests**: Cliente HTTP
- **python-dotenv**: Variables de entorno
- **gunicorn**: Servidor WSGI (producción)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
