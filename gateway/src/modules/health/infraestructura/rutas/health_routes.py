from flask import Blueprint
from modules.health.infraestructura.cmd.health_cmd import HealthCmd


def create_health_routes(health_controller: HealthCmd) -> Blueprint:
    """
    Crea y configura las rutas relacionadas con health check.
    
    Args:
        health_controller: Instancia del controlador de salud
        
    Returns:
        Blueprint: Blueprint de Flask con las rutas configuradas
    """
    health_bp = Blueprint('health', __name__, url_prefix='/health')
    
    @health_bp.route('/', methods=['GET'])
    def check():
        """Endpoint principal de health check."""
        return health_controller.get_health()
    
    return health_bp