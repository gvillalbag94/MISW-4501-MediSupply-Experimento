"""
Entidades del dominio del módulo de autorización refactorizado.
"""

from .token_payload import TokenPayload, Role
from .resource import ResourceType, ActionType, AccessRequest, RolePermissions

__all__ = [
    "TokenPayload",
    "Role", 
    "ResourceType",
    "ActionType",
    "AccessRequest",
    "RolePermissions"
]