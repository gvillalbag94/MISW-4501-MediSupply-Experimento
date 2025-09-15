from flask import Blueprint, request
from ..cmd.auth_cmd import AuthCmd


def create_auth_routes(auth_controller: AuthCmd) -> Blueprint:
    """
    Crea y configura las rutas relacionadas con autenticación y autorización.
    
    Args:
        auth_controller: Instancia del controlador de autenticación
        
    Returns:
        Blueprint: Blueprint de Flask con las rutas configuradas
    """
    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
    
    @auth_bp.route('/validate', methods=['POST'])
    def validate_token():
        """Endpoint para validar un token."""
        return auth_controller.validate_token()
    
    @auth_bp.route('/authorize', methods=['POST'])
    def authorize_access():
        """Endpoint para autorizar acceso a rutas específicas."""
        return auth_controller.authorize_access()
    
    @auth_bp.route('/user-info', methods=['POST'])
    def get_user_info():
        """Endpoint para obtener información del usuario."""
        return auth_controller.get_user_info()
    
    @auth_bp.route('/resources', methods=['GET'])
    def get_resources():
        """Endpoint para obtener la lista de recursos disponibles en el microservicio de productos."""
        return {
            "microservice": "productos",
            "resources": [
                {"name": "productos", "description": "Gestión de productos"},
                {"name": "health", "description": "Verificación de salud"},
                {"name": "auth", "description": "Validación de autorización"}
            ],
            "actions": [
                {"name": "create", "description": "Crear recurso"},
                {"name": "read", "description": "Leer recurso"},
                {"name": "update", "description": "Actualizar recurso"},
                {"name": "delete", "description": "Eliminar recurso"}
            ],
            "endpoints": [
                {"path": "/auth/validate", "method": "POST", "description": "Validar token"},
                {"path": "/auth/authorize", "method": "POST", "description": "Autorizar acceso"},
                {"path": "/auth/user-info", "method": "POST", "description": "Obtener info del usuario"}
            ]
        }, 200
    
    return auth_bp