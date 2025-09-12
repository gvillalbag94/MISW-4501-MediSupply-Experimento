from flask import Blueprint, request
from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd


def create_auth_routes(auth_controller: AuthCmd) -> Blueprint:
    """
    Crea y configura las rutas relacionadas con autenticación.
    
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
        email = data.get("email")
        password = data.get("password")
        return auth_controller.login(email, password)
    
    return auth_bp