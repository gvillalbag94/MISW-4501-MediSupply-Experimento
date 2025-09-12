from typing import List, Optional
from decimal import Decimal
from src.dominio.entities.producto import Producto, Categoria
from src.dominio.repositorios.producto_repository import ProductoRepository


class ProductoRepositoryImpl(ProductoRepository):
    """Implementación del repositorio de productos con datos en memoria."""
    
    def __init__(self):
        # Datos de ejemplo en memoria
        self._productos = [
            Producto(
                id="1",
                nombre="iPhone 15",
                descripcion="Último modelo de iPhone con cámara mejorada",
                precio=Decimal("999.99"),
                categoria=Categoria.ELECTRONICOS,
                stock=50,
                activo=True
            ),
            Producto(
                id="2",
                nombre="Samsung Galaxy S24",
                descripcion="Smartphone Android de última generación",
                precio=Decimal("899.99"),
                categoria=Categoria.ELECTRONICOS,
                stock=30,
                activo=True
            ),
            Producto(
                id="3",
                nombre="Camiseta Nike",
                descripcion="Camiseta deportiva de algodón",
                precio=Decimal("29.99"),
                categoria=Categoria.ROPA,
                stock=100,
                activo=True
            ),
            Producto(
                id="4",
                nombre="Sofá 3 plazas",
                descripcion="Sofá cómodo para sala de estar",
                precio=Decimal("599.99"),
                categoria=Categoria.HOGAR,
                stock=10,
                activo=True
            ),
            Producto(
                id="5",
                nombre="Pelota de Fútbol",
                descripcion="Pelota oficial de fútbol",
                precio=Decimal("24.99"),
                categoria=Categoria.DEPORTES,
                stock=75,
                activo=True
            ),
            Producto(
                id="6",
                nombre="Clean Code",
                descripcion="Libro sobre buenas prácticas de programación",
                precio=Decimal("39.99"),
                categoria=Categoria.LIBROS,
                stock=25,
                activo=True
            )
        ]
    
    def obtener_todos(self) -> List[Producto]:
        """Obtiene todos los productos."""
        return self._productos.copy()
    
    def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        for producto in self._productos:
            if producto.id == producto_id:
                return producto
        return None
    
    def obtener_por_categoria(self, categoria: str) -> List[Producto]:
        """Obtiene productos por categoría."""
        return [p for p in self._productos if p.categoria.value == categoria]
    
    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """Busca productos por nombre."""
        nombre_lower = nombre.lower()
        return [p for p in self._productos if nombre_lower in p.nombre.lower()]
