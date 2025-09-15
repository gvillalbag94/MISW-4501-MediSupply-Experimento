from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass(frozen=True)
class Token:
    """
    Entidad del dominio que representa un token de autenticación.
    """
    id: str
    user_id: str
    token_value: str
    token_type: TokenType
    expires_at: datetime
    created_at: datetime
    status: TokenStatus
    permissions: Optional[str] = None  # JSON string of permissions
    
    def is_valid(self) -> bool:
        """Verifica si el token es válido."""
        return (
            self.status == TokenStatus.ACTIVE and
            self.expires_at > datetime.utcnow()
        )
    
    def is_expired(self) -> bool:
        """Verifica si el token ha expirado."""
        return self.expires_at <= datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token_value": self.token_value,
            "token_type": self.token_type.value,
            "expires_at": self.expires_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "status": self.status.value,
            "permissions": self.permissions
        }
