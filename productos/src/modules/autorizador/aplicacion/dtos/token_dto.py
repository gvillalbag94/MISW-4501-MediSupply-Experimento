from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TokenDto:
    """DTO para transferir información de tokens."""
    id: str
    user_id: str
    token_value: str
    token_type: str
    expires_at: datetime
    created_at: datetime
    status: str
    permissions: Optional[str] = None


@dataclass
class AuthorizationRequestDto:
    """DTO para solicitudes de autorización."""
    token: str
    resource: str
    action: str


@dataclass
class AuthorizationResponseDto:
    """DTO para respuestas de autorización."""
    authorized: bool
    user_id: str
    user_role: str
    message: Optional[str] = None
