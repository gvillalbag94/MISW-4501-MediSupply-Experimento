from modules.health.dominio.entities import Health
from modules.health.dominio.repositorios import HealthRepository

class HealthRepositoryImpl(HealthRepository):

    def __init__(self):
        pass

    def get_health(self):
        try:
            return Health.healthy()
        except Exception as e:
            return Health.unhealthy()