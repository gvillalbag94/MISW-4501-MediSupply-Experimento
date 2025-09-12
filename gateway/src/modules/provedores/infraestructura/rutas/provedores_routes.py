import requests
from flask import Blueprint, request, jsonify
import os

def create_provedores_routes() -> Blueprint:
    """
    Crea las rutas para provedores que hacen proxy al microservicio.
    """

    provedores_routes = Blueprint("provedores", __name__, url_prefix="/provedores")

    PROVEDORES_SERVICE_URL = os.environ.get("PROVEDORES_SERVICE_URL", "http://localhost:5003")

    def make_request_to_provedores(endpoint, method="GET", params=None, data=None, headers=None):
        """Hace una petición al microservicio de provedores."""
        try:
            url = f"{PROVEDORES_SERVICE_URL}{endpoint}"
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
                "error": f"Error conectando con el servicio de provedores: {str(e)}"
            }), 503

    @provedores_routes.route("", methods=["GET"])
    def obtener_todos_los_provedores():
        """Obtiene todos los provedores."""
        headers = request.headers
        return make_request_to_provedores("/provedores", headers=headers)

    @provedores_routes.route("/<string:provedor_id>", methods=["GET"])
    def obtener_provedor_por_id(provedor_id: str):
        """Obtiene un provedor por su ID."""
        headers = request.headers
        return make_request_to_provedores(f"/provedores/{provedor_id}", headers=headers)

    return provedores_routes
