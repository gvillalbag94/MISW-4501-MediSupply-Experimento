from flask import Blueprint, request
from src.infraestructura.cmd.provedor_cmd import ProvedorCmd


def create_provedor_routes(provedor_controller: ProvedorCmd) -> Blueprint:
    """Crea las rutas para proveedores."""

    provedor_routes = Blueprint("provedores", __name__, url_prefix="/provedores")
    
    @provedor_routes.route("", methods=["GET"])
    def obtener_todos_los_provedores():
        """Obtiene todos los proveedores."""
        return provedor_controller.obtener_todos_los_provedores()
    
    @provedor_routes.route("/<int:provedor_id>", methods=["GET"])
    def obtener_provedor_por_id(provedor_id: int):
        """Obtiene un proveedor por su ID."""
        return provedor_controller.obtener_provedor_por_id(provedor_id)
    
    @provedor_routes.route("/nit/<int:nit>", methods=["GET"])
    def obtener_provedor_por_nit(nit: int):
        """Obtiene un proveedor por su NIT."""
        return provedor_controller.obtener_provedor_por_nit(nit)
    
    @provedor_routes.route("/pais/<string:pais>", methods=["GET"])
    def obtener_provedores_por_pais(pais: str):
        """Obtiene proveedores por país."""
        return provedor_controller.obtener_provedores_por_pais(pais)
    
    @provedor_routes.route("/buscar", methods=["GET"])
    def buscar_provedores_por_nombre():
        """Busca proveedores por nombre."""
        nombre = request.args.get("nombre", "")
        if not nombre:
            return {
                "success": False,
                "error": "Parámetro nombre es requerido"
            }, 400
        
        return provedor_controller.buscar_provedores_por_nombre(nombre)
    
    return provedor_routes
