import requests
from flask import Blueprint, request, jsonify
import os

def create_producto_routes() -> Blueprint:
    """
    Crea las rutas para productos que hacen proxy al microservicio.
    """

    producto_routes = Blueprint("productos", __name__, url_prefix="/productos")

    PRODUCTOS_SERVICE_URL = os.environ.get("PRODUCTOS_SERVICE_URL", "http://localhost:5002")

    def make_request_to_productos(endpoint, method="GET", params=None, data=None, headers=None):
        """Hace una petición al microservicio de productos."""
        try:
            url = f"{PRODUCTOS_SERVICE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                return jsonify({"error": "Método no soportado"}), 405

            return response.json(), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de productos: {str(e)}"
            }), 503

    @producto_routes.route("", methods=["GET"])
    def obtener_todos_los_productos():
        """Obtiene todos los productos."""
        headers = request.headers
        return make_request_to_productos("/productos", headers=headers)

    @producto_routes.route("/<string:producto_id>", methods=["GET"])
    def obtener_producto_por_id(producto_id: str):
        """Obtiene un producto por su ID."""
        headers = request.headers
        return make_request_to_productos(f"/productos/{producto_id}", headers=headers)

    return producto_routes
