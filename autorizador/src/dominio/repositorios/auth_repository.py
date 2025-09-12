from abc import ABC, abstractmethod

from modules.autenticador.aplicacion.dtos.session_dto import SessionDto

class AuthRepository(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> SessionDto: ...