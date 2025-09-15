"""
Entidades para recursos y acciones del sistema.
"""
from enum import Enum
from dataclasses import dataclass
from typing import List
from .token_payload import Role


class ResourceType(Enum):
    """Tipos de recursos en el sistema."""
    PRODUCTS = "productos"
    PROVIDERS = "provedores"
    USERS = "users"
    HEALTH = "health"
    AUTH = "auth"


class ActionType(Enum):
    """Tipos de acciones sobre recursos."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"


@dataclass
class AccessRequest:
    """
    Representa una solicitud de acceso a un recurso.
    """
    resource: ResourceType
    action: ActionType
    user_role: Role
    
    def __str__(self) -> str:
        return f"{self.user_role.value} -> {self.action.value} on {self.resource.value}"


class RolePermissions:
    """
    Define los permisos por rol de manera estática.
    """
    
    PERMISSIONS = {
        # ADMIN: Acceso completo a productos y provedores
        Role.ADMIN: {
            ResourceType.PRODUCTS: [ActionType.CREATE, ActionType.READ, ActionType.UPDATE, ActionType.DELETE],
            ResourceType.PROVIDERS: [ActionType.CREATE, ActionType.READ, ActionType.UPDATE, ActionType.DELETE],
            ResourceType.USERS: [ActionType.CREATE, ActionType.READ, ActionType.UPDATE, ActionType.DELETE],
            ResourceType.HEALTH: [ActionType.READ],
            ResourceType.AUTH: [ActionType.EXECUTE]
        },
        # USER: Solo acceso a productos (todas las operaciones)
        Role.USER: {
            ResourceType.PRODUCTS: [ActionType.CREATE, ActionType.READ, ActionType.UPDATE, ActionType.DELETE]
            # SIN acceso a PROVIDERS
        },
        Role.MANAGER: {
            ResourceType.PRODUCTS: [ActionType.CREATE, ActionType.READ, ActionType.UPDATE, ActionType.DELETE],
            ResourceType.PROVIDERS: [ActionType.CREATE, ActionType.READ, ActionType.UPDATE, ActionType.DELETE],
            ResourceType.USERS: [ActionType.READ],
            ResourceType.HEALTH: [ActionType.READ],
            ResourceType.AUTH: [ActionType.EXECUTE]
        },
        Role.VIEWER: {
            ResourceType.PRODUCTS: [ActionType.READ],
            ResourceType.HEALTH: [ActionType.READ]
            # SIN acceso a PROVIDERS
        }
    }
    
    @classmethod
    def can_access(cls, role: Role, resource: ResourceType, action: ActionType) -> bool:
        """
        Verifica si un rol puede realizar una acción sobre un recurso.
        """
        # Obtener permisos del rol
        role_permissions = cls.PERMISSIONS.get(role, {})
        
        # Si no hay permisos definidos para el rol
        if not role_permissions:
            return False
        
        # Obtener acciones permitidas para el recurso
        allowed_actions = role_permissions.get(resource, [])
        
        # Verificar si la acción está permitida
        return action in allowed_actions
