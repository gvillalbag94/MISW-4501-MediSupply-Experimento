from modules.health.dominio.entities import Health
from modules.health.dominio.repositorios import HealthRepository

class HealthService:
    def __init__(self, health_repository: HealthRepository):
        self.health_repository = health_repository

    def get_health(self) -> Health:
        try:
            return Health.healthy()
        except Exception as e:
            return Health.unhealthy()