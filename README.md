# Sistema de Microservicios con API Gateway

Este proyecto implementa un sistema de microservicios con un API Gateway que actúa como punto de entrada único.

## Arquitectura

El sistema está compuesto por:

1. **API Gateway** (Puerto 5000): Punto de entrada único que enruta las peticiones a los microservicios
2. **Microservicio de Autenticación** (Puerto 5002): Maneja la autenticación de usuarios
3. **Microservicio de Productos** (Puerto 5001): Gestiona el catálogo de productos

## Servicios Disponibles

### API Gateway
- **URL**: http://localhost:5000
- **Health Check**: http://localhost:5000/health/
- **Funcionalidades**:
  - Proxy a microservicio de autenticación
  - Proxy a microservicio de productos
  - Health check del sistema

### Microservicio de Productos
- **URL**: http://localhost:5001
- **Health Check**: http://localhost:5001/health
- **Endpoints**:
  - `GET /productos` - Lista todos los productos
  - `GET /productos/{id}` - Obtiene un producto por ID
  - `GET /productos/categoria/{categoria}` - Filtra por categoría
  - `GET /productos/buscar?nombre={nombre}` - Busca por nombre

### Microservicio de Autenticación
- **URL**: http://localhost:5002
- **Funcionalidades**:
  - Login de usuarios
  - Generación de tokens JWT

## Instalación y Ejecución

### Requisitos
- Python 3.9+
- pipenv
- Docker (opcional)

### Ejecución Individual

#### 1. Microservicio de Productos
```bash
cd productos
pipenv install
pipenv run python src/main.py
```

#### 2. API Gateway
```bash
cd gateway
pipenv install
pipenv run python src/main.py
```

### Ejecución con Docker Compose
```bash
docker-compose up --build
```

## Pruebas

### Probar Microservicio de Productos
```bash
cd productos
./test_productos.sh
```

### Probar Integración Completa
```bash
cd gateway
./test_gateway_integration.sh
```

## Endpoints de Productos

### A través del API Gateway (Recomendado)
- `GET http://localhost:5000/productos`
- `GET http://localhost:5000/productos/1`
- `GET http://localhost:5000/productos/categoria/electronicos`
- `GET http://localhost:5000/productos/buscar?nombre=iPhone`

### Directamente al Microservicio
- `GET http://localhost:5001/productos`
- `GET http://localhost:5001/productos/1`
- `GET http://localhost:5001/productos/categoria/electronicos`
- `GET http://localhost:5001/productos/buscar?nombre=iPhone`

## Categorías de Productos Disponibles

- `electronicos`
- `ropa`
- `hogar`
- `deportes`
- `libros`
- `otros`

## Estructura del Proyecto

```
experimento_1/
├── gateway/                 # API Gateway
│   ├── src/
│   │   ├── config/         # Configuración
│   │   └── modules/        # Módulos del gateway
│   └── Dockerfile
├── productos/              # Microservicio de Productos
│   ├── src/
│   │   ├── dominio/        # Entidades y repositorios
│   │   ├── aplicacion/     # DTOs, mappers, servicios, casos de uso
│   │   └── infraestructura/ # Controladores, rutas, configuración
│   └── Dockerfile
├── autorizador/            # Microservicio de Autenticación
└── docker-compose.yml      # Orquestación de servicios
```

## Arquitectura Hexagonal

El microservicio de productos sigue los principios de arquitectura hexagonal (Clean Architecture):

- **Dominio**: Entidades y reglas de negocio
- **Aplicación**: Casos de uso, servicios y DTOs
- **Infraestructura**: Controladores, repositorios y rutas

## Variables de Entorno

### Gateway
- `PRODUCTOS_SERVICE_URL`: URL del microservicio de productos
- `JWT_SECRET`: Clave secreta para JWT
- `ALGORITHM`: Algoritmo de encriptación

### Productos
- `PORT`: Puerto del microservicio (default: 5001)
- `DEBUG`: Modo debug (default: true)
- `LOG_LEVEL`: Nivel de logging (default: INFO)

## Desarrollo

### Agregar Nuevos Endpoints
1. Definir la entidad en `dominio/entities/`
2. Crear el DTO en `aplicacion/dtos/`
3. Implementar el mapper en `aplicacion/mappers/`
4. Crear el servicio en `aplicacion/servicios/`
5. Implementar el caso de uso en `aplicacion/use_cases/`
6. Crear el controlador en `infraestructura/cmd/`
7. Definir las rutas en `infraestructura/rutas/`
8. Registrar las rutas en `infraestructura/config/config.py`

### Agregar Nuevos Microservicios al Gateway
1. Crear el módulo en `gateway/src/modules/`
2. Implementar las rutas de proxy
3. Registrar las rutas en `gateway/src/config/config.py`
4. Actualizar `docker-compose.yml`
