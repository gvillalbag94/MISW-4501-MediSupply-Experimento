# Microservicio de Provedores

Este microservicio maneja la gestión de proveedores siguiendo los principios de arquitectura hexagonal.

## Estructura del Proyecto

```
src/
├── dominio/
│   ├── entities/
│   │   └── provedor.py          # Entidad Provedor
│   └── repositorios/
│       └── provedor_repository.py  # Interfaz del repositorio
├── aplicacion/
│   ├── dtos/
│   │   └── provedor_dto.py      # DTOs para transferencia de datos
│   ├── mappers/
│   │   └── provedor_mapper.py   # Mappers entre entidades y DTOs
│   ├── servicios/
│   │   └── provedor_service.py  # Servicios de dominio
│   └── use_cases/
│       └── provedor_use_case.py # Casos de uso
└── infraestructura/
    ├── cmd/
    │   └── provedor_cmd.py      # Controladores (comandos)
    ├── config/
    │   └── config.py            # Configuración de la aplicación
    ├── repositorios/
    │   └── provedor_repository.py  # Implementación del repositorio
    └── rutas/
        └── provedor_routes.py   # Definición de rutas REST
```

## Entidad Provedor

La entidad Provedor tiene los siguientes campos:
- `id`: int - Identificador único
- `nit`: int - Número de identificación tributaria
- `nombre`: str - Nombre del proveedor
- `pais`: Pais - País del proveedor (enum)
- `direccion`: str - Dirección del proveedor
- `telefono`: int - Número de teléfono
- `email`: str - Correo electrónico

## Endpoints Disponibles

- `GET /provedores` - Obtiene todos los proveedores
- `GET /provedores/{id}` - Obtiene un proveedor por ID
- `GET /provedores/nit/{nit}` - Obtiene un proveedor por NIT
- `GET /provedores/pais/{pais}` - Obtiene proveedores por país
- `GET /provedores/buscar?nombre={nombre}` - Busca proveedores por nombre
- `GET /health` - Health check del servicio

## Ejecución

### Desarrollo Local
```bash
pipenv install
pipenv run python src/main.py
```

### Docker
```bash
docker build -t provedores .
docker run -p 5003:5003 provedores
```

## Puerto

El microservicio se ejecuta en el puerto **5003** por defecto.
