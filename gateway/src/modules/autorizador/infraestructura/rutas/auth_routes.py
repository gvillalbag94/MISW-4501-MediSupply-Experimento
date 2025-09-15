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
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Endpoint para iniciar sesión."""
        data = request.get_json()
        if not data:
            return {"error": "Datos requeridos"}, 400
        
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return {"error": "Email y contraseña requeridos"}, 400
        
        return auth_controller.login(email, password)
    
    @auth_bp.route('/logout', methods=['POST'])
    def logout():
        """Endpoint para cerrar sesión."""
        return auth_controller.logout()
    
    @auth_bp.route('/validate', methods=['POST'])
    def validate_token():
        """Endpoint para validar un token."""
        return auth_controller.validate_token()
    
    @auth_bp.route('/authorize', methods=['POST'])
    def authorize():
        """Endpoint para autorizar acceso a recursos."""
        return auth_controller.authorize()
    
    @auth_bp.route('/admin-check', methods=['POST'])
    def check_admin():
        """Endpoint para verificar acceso de administrador."""
        return auth_controller.check_admin()
    
    @auth_bp.route('/resources', methods=['GET'])
    def get_resources():
        """Endpoint para obtener la lista de recursos disponibles."""
        return {
            "resources": [
                {"name": "users", "description": "Gestión de usuarios"},
                {"name": "productos", "description": "Gestión de productos"},
                {"name": "provedores", "description": "Gestión de proveedores"},
                {"name": "health", "description": "Verificación de salud"},
                {"name": "auth", "description": "Autenticación y autorización"}
            ],
            "actions": [
                {"name": "create", "description": "Crear recurso"},
                {"name": "read", "description": "Leer recurso"},
                {"name": "update", "description": "Actualizar recurso"},
                {"name": "delete", "description": "Eliminar recurso"},
                {"name": "execute", "description": "Ejecutar acción"}
            ]
        }, 200
    
    return auth_bp