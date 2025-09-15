"""
Entidad para representar el payload de un token JWT.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class Role(Enum):
    """Roles disponibles en el sistema."""
    ADMIN = "admin"
    MANAGER = "manager"  
    USER = "user"
    VIEWER = "viewer"


@dataclass
class TokenPayload:
    """
    Representa el contenido de un token JWT decodificado.
    """
    user_id: str
    role: Role
    exp: datetime
    iat: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TokenPayload':
        """Crea TokenPayload desde diccionario JWT."""
        return cls(
            user_id=str(data['user_id']),
            role=Role(data['role']),
            exp=datetime.utcfromtimestamp(data['exp']),
            iat=datetime.utcfromtimestamp(data['iat']) if 'iat' in data else None
        )
    
    def is_expired(self) -> bool:
        """Verifica si el token ha expirado."""
        return datetime.utcnow() > self.exp
    
    def has_role(self, required_role: Role) -> bool:
        """Verifica si el usuario tiene el rol requerido."""
        return self.role == required_role
    
    def has_admin_access(self) -> bool:
        """Verifica si el usuario tiene acceso de administrador."""
        return self.role == Role.ADMIN
