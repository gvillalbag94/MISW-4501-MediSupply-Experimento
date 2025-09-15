
from dataclasses import dataclass
from enum import Enum
from modules.autenticador.dominio.entities.user import Role


class RoleDto(Enum):
    ADMIN = "admin"
    USER = "user"   

@dataclass(frozen=True)
class UserDto:
    """
    DTO que representa el usuario.
    """
    id: str
    name: str
    email: str
    password: str
    role: RoleDto
    token: str