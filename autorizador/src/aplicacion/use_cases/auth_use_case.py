from modules.autenticador.aplicacion.servicios.auth_service import AuthService
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto

class AuthUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def execute(self, email: str, password: str) -> SessionDto:
        user = self.auth_service.login(email, password)
        if user:
            return user
        else:
            return None