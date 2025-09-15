from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Set


class ResourceType(Enum):
    USERS = "users"
    PRODUCTS = "productos"
    PROVIDERS = "provedores"
    HEALTH = "health"
    AUTH = "auth"
    ALL = "*"


class ActionType(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    ALL = "*"


@dataclass(frozen=True)
class Permission:
    """
    Entidad del dominio que representa un permiso.
    """
    id: str
    name: str
    resource: ResourceType
    action: ActionType
    description: str
    
    def matches(self, resource: ResourceType, action: ActionType) -> bool:
        """Verifica si este permiso concede acceso al recurso y acción especificados."""
        resource_match = (
            self.resource == resource or 
            self.resource == ResourceType.ALL
        )
        action_match = (
            self.action == action or 
            self.action == ActionType.ALL
        )
        return resource_match and action_match
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "resource": self.resource.value,
            "action": self.action.value,
            "description": self.description
        }


@dataclass(frozen=True)
class PermissionSet:
    """
    Conjunto de permisos para facilitar las verificaciones.
    """
    permissions: Set[Permission]
    
    def has_permission(self, resource: ResourceType, action: ActionType) -> bool:
        """Verifica si el conjunto contiene un permiso para el recurso y acción."""
        return any(
            permission.matches(resource, action) 
            for permission in self.permissions
        )
    
    def add_permission(self, permission: Permission) -> 'PermissionSet':
        """Añade un permiso al conjunto (inmutable)."""
        new_permissions = self.permissions.copy()
        new_permissions.add(permission)
        return PermissionSet(new_permissions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el conjunto a diccionario."""
        return {
            "permissions": [p.to_dict() for p in self.permissions]
        }
