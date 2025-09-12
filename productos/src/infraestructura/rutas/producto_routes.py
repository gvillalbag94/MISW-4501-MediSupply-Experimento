from flask import Blueprint, request
from src.infraestructura.cmd.producto_cmd import ProductoCmd


def create_producto_routes(producto_controller: ProductoCmd) -> Blueprint:
    """Crea las rutas para productos."""

    producto_routes = Blueprint("productos", __name__, url_prefix="/productos")
    
    @producto_routes.route("", methods=["GET"])
    def obtener_todos_los_productos():
        """Obtiene todos los productos."""
        return producto_controller.obtener_todos_los_productos()
    
    @producto_routes.route("/<string:producto_id>", methods=["GET"])
    def obtener_producto_por_id(producto_id: str):
        """Obtiene un producto por su ID."""
        return producto_controller.obtener_producto_por_id(producto_id)
    
    @producto_routes.route("/categoria/<string:categoria>", methods=["GET"])
    def obtener_productos_por_categoria(categoria: str):
        """Obtiene productos por categoría."""
        return producto_controller.obtener_productos_por_categoria(categoria)
    
    @producto_routes.route("/buscar", methods=["GET"])
    def buscar_productos_por_nombre():
        """Busca productos por nombre."""
        nombre = request.args.get("nombre", "")
        if not nombre:
            return {
                "success": False,
                "error": "Parámetro nombre es requerido"
            }, 400
        
        return producto_controller.buscar_productos_por_nombre(nombre)
    
    return producto_routes
