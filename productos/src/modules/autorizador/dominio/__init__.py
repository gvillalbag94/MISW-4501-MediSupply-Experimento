"""
Dominio del módulo de autorización refactorizado.
"""

from .entities import (
    TokenPayload,
    Role,
    ResourceType,
    ActionType,
    AccessRequest,
    RolePermissions
)

from .exceptions import (
    AuthorizationError,
    InvalidTokenError,
    ExpiredTokenError,
    InsufficientPermissionsError,
    MissingTokenError
)

__all__ = [
    # Entidades
    "TokenPayload",
    "Role",
    "ResourceType", 
    "ActionType",
    "AccessRequest",
    "RolePermissions",
    
    # Excepciones
    "AuthorizationError",
    "InvalidTokenError",
    "ExpiredTokenError", 
    "InsufficientPermissionsError",
    "MissingTokenError"
]
