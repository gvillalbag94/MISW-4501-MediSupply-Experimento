# Microservicio de Productos

Este microservicio maneja la gestión de productos siguiendo la arquitectura hexagonal.

## Características

- Lista todos los productos
- Obtiene un producto por ID
- Filtra productos por categoría
- Busca productos por nombre
- Arquitectura hexagonal (Clean Architecture)
- Datos en memoria para simplicidad

## Estructura del Proyecto

```
src/
├── dominio/
│   ├── entities/
│   │   └── producto.py          # Entidad Producto
│   └── repositorios/
│       └── producto_repository.py # Interfaz del repositorio
├── aplicacion/
│   ├── dtos/
│   │   └── producto_dto.py      # DTOs para transferencia de datos
│   ├── mappers/
│   │   └── producto_mapper.py   # Mappers entre entidades y DTOs
│   ├── servicios/
│   │   └── producto_service.py  # Servicios de dominio
│   └── use_cases/
│       └── producto_use_case.py # Casos de uso
└── infraestructura/
    ├── cmd/
    │   └── producto_cmd.py      # Controladores
    ├── config/
    │   └── config.py            # Configuración de la aplicación
    ├── repositorios/
    │   └── producto_repository.py # Implementación del repositorio
    └── rutas/
        └── producto_routes.py   # Definición de rutas
```

## Endpoints Disponibles

### GET /productos
Obtiene todos los productos disponibles.

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "nombre": "iPhone 15",
      "descripcion": "Último modelo de iPhone con cámara mejorada",
      "precio": 999.99,
      "categoria": "electronicos",
      "stock": 50,
      "activo": true
    }
  ],
  "total": 6
}
```

### GET /productos/{id}
Obtiene un producto específico por su ID.

### GET /productos/categoria/{categoria}
Filtra productos por categoría.

Categorías disponibles:
- electronicos
- ropa
- hogar
- deportes
- libros
- otros

### GET /productos/buscar?nombre={nombre}
Busca productos por nombre.

## Instalación y Ejecución

### Requisitos
- Python 3.9+
- pipenv

### Instalación
```bash
pipenv install
```

### Ejecución
```bash
pipenv run python src/main.py
```

El servicio estará disponible en `http://localhost:5001`

### Health Check
```bash
curl http://localhost:5001/health
```

## Variables de Entorno

- `ENV`: Entorno de ejecución (default: development)
- `DEBUG`: Modo debug (default: true)
- `HOST`: Host de la aplicación (default: 0.0.0.0)
- `PORT`: Puerto de la aplicación (default: 5001)
- `LOG_LEVEL`: Nivel de logging (default: INFO)

## Docker

### Construir imagen
```bash
docker build -t microservicio-productos .
```

### Ejecutar contenedor
```bash
docker run -p 5001:5001 microservicio-productos
```

## Integración con API Gateway

Este microservicio está diseñado para ser consumido a través del API Gateway en el puerto 5000. El gateway actúa como proxy y enruta las peticiones a este microservicio.
