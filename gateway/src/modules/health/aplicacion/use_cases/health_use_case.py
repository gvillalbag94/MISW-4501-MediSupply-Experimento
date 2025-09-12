from modules.health.aplicacion.servicios.health_service import HealthService
from modules.health.dominio.entities.health import Health

class HealthUseCase:
    def __init__(self, health_service: HealthService):
        self.health_service = health_service

    def execute(self) -> Health:
        return self.health_service.get_health()