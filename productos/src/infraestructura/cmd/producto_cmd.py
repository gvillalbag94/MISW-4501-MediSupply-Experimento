from flask import jsonify
from typing import List, Optional
from src.aplicacion.use_cases.producto_use_case import ProductoUseCase
from src.aplicacion.mappers.producto_mapper import ProductoMapper
from src.dominio.entities.producto import Producto


class ProductoCmd:
    """Controlador para productos."""
    
    def __init__(self, producto_use_case: ProductoUseCase):
        self.producto_use_case = producto_use_case
    
    def obtener_todos_los_productos(self):
        """Obtiene todos los productos."""
        try:
            productos = self.producto_use_case.obtener_todos_los_productos()
            productos_dto = [ProductoMapper.entity_to_dto(p) for p in productos]
            productos_json = [ProductoMapper.dto_to_json(p) for p in productos_dto]
            
            return jsonify({
                "success": True,
                "data": productos_json,
                "total": len(productos_json)
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def obtener_producto_por_id(self, producto_id: str):
        """Obtiene un producto por su ID."""
        try:
            producto = self.producto_use_case.obtener_producto_por_id(producto_id)
            if not producto:
                return jsonify({
                    "success": False,
                    "error": "Producto no encontrado"
                }), 404
            
            producto_dto = ProductoMapper.entity_to_dto(producto)
            producto_json = ProductoMapper.dto_to_json(producto_dto)
            
            return jsonify({
                "success": True,
                "data": producto_json
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def obtener_productos_por_categoria(self, categoria: str):
        """Obtiene productos por categoría."""
        try:
            productos = self.producto_use_case.obtener_productos_por_categoria(categoria)
            productos_dto = [ProductoMapper.entity_to_dto(p) for p in productos]
            productos_json = [ProductoMapper.dto_to_json(p) for p in productos_dto]
            
            return jsonify({
                "success": True,
                "data": productos_json,
                "total": len(productos_json),
                "categoria": categoria
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def buscar_productos_por_nombre(self, nombre: str):
        """Busca productos por nombre."""
        try:
            productos = self.producto_use_case.buscar_productos_por_nombre(nombre)
            productos_dto = [ProductoMapper.entity_to_dto(p) for p in productos]
            productos_json = [ProductoMapper.dto_to_json(p) for p in productos_dto]
            
            return jsonify({
                "success": True,
                "data": productos_json,
                "total": len(productos_json),
                "busqueda": nombre
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
