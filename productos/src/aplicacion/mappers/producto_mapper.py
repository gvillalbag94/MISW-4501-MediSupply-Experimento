from typing import Dict, Any
from decimal import Decimal
from src.dominio.entities.producto import Producto, Categoria
from src.aplicacion.dtos.producto_dto import ProductoDto, CategoriaDto


class ProductoMapper:
    @staticmethod
    def json_to_dto(producto: Dict[str, Any]) -> ProductoDto:
        return ProductoDto(
            id=producto["id"],
            nombre=producto["nombre"],
            descripcion=producto["descripcion"],
            precio=producto["precio"],
            categoria=CategoriaDto(producto["categoria"]),
            stock=producto["stock"],
            activo=producto.get("activo", True),
        )   
    
    @staticmethod
    def dto_to_json(producto_dto: ProductoDto) -> Dict[str, Any]:
        return {
            "id": producto_dto.id,
            "nombre": producto_dto.nombre,
            "descripcion": producto_dto.descripcion,
            "precio": producto_dto.precio,
            "categoria": producto_dto.categoria.value,
            "stock": producto_dto.stock,
            "activo": producto_dto.activo,
        }
    
    @staticmethod
    def dto_to_entity(producto_dto: ProductoDto) -> Producto:
        categoria = Categoria(producto_dto.categoria.value)
        return Producto(
            id=producto_dto.id,
            nombre=producto_dto.nombre,
            descripcion=producto_dto.descripcion,
            precio=Decimal(str(producto_dto.precio)),
            categoria=categoria,
            stock=producto_dto.stock,
            activo=producto_dto.activo,
        )
    
    @staticmethod
    def entity_to_dto(producto: Producto) -> ProductoDto:
        categoria = CategoriaDto(producto.categoria.value)
        return ProductoDto(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=float(producto.precio),
            categoria=categoria,
            stock=producto.stock,
            activo=producto.activo,
        )
