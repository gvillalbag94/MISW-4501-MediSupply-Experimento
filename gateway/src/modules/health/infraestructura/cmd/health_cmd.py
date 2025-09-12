from modules.health.aplicacion import HealthUseCase
from modules.health.dominio.entities import Health
from flask import Response, jsonify

class HealthCmd:
    def __init__(self, health_use_case: HealthUseCase):
        self.health_use_case = health_use_case

    def get_health(self) -> Response:
        try:
            health = self.health_use_case.execute()
            return jsonify(health.__dict__), 200
        except Exception as e:
            error_message = Health.unhealthy().to_dict()
            return jsonify(error_message), 500