from typing import List, Optional
from src.aplicacion.servicios.producto_service import ProductoService
from src.dominio.entities.producto import Producto


class ProductoUseCase:
    """Caso de uso para productos."""
    
    def __init__(self, producto_service: ProductoService):
        self.producto_service = producto_service
    
    def obtener_todos_los_productos(self) -> List[Producto]:
        """Obtiene todos los productos."""
        return self.producto_service.obtener_todos_los_productos()
    
    def obtener_producto_por_id(self, producto_id: str) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        return self.producto_service.obtener_producto_por_id(producto_id)
    
    def obtener_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """Obtiene productos por categoría."""
        return self.producto_service.obtener_productos_por_categoria(categoria)
    
    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """Busca productos por nombre."""
        return self.producto_service.buscar_productos_por_nombre(nombre)
