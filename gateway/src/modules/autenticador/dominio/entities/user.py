from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class Role(Enum):
    ADMIN = "admin"
    USER = "user"   


@dataclass(frozen=True)
class User:
    """
    Entidad del dominio que representa el usuario.
    """
    id: str
    name: str
    email: str
    password: str
    role: Role
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role.value,
        }