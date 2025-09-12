from typing import List, Optional
from src.dominio.entities.producto import Producto, Categoria
from src.dominio.repositorios.producto_repository import ProductoRepository


class ProductoService:
    """Servicio de dominio para productos."""
    
    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository
    
    def obtener_todos_los_productos(self) -> List[Producto]:
        """Obtiene todos los productos activos."""
        productos = self.producto_repository.obtener_todos()
        return [p for p in productos if p.activo]
    
    def obtener_producto_por_id(self, producto_id: str) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        return self.producto_repository.obtener_por_id(producto_id)
    
    def obtener_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """Obtiene productos por categoría."""
        try:
            categoria_enum = Categoria(categoria)
            productos = self.producto_repository.obtener_por_categoria(categoria)
            return [p for p in productos if p.activo]
        except ValueError:
            return []
    
    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """Busca productos por nombre."""
        productos = self.producto_repository.buscar_por_nombre(nombre)
        return [p for p in productos if p.activo]
