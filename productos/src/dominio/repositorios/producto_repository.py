from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.entities.producto import Producto


class ProductoRepository(ABC):
    """Interfaz del repositorio de productos."""
    
    @abstractmethod
    def obtener_todos(self) -> List[Producto]:
        """Obtiene todos los productos."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        pass
    
    @abstractmethod
    def obtener_por_categoria(self, categoria: str) -> List[Producto]:
        """Obtiene productos por categoría."""
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """Busca productos por nombre."""
        pass
