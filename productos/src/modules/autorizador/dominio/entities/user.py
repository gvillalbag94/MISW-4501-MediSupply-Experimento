from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Set, Optional
from .permission import Permission, PermissionSet, ResourceType, ActionType


class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
    VIEWER = "viewer"


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
    is_active: bool = True
    permissions: Optional[PermissionSet] = None
    
    def has_permission(self, resource: ResourceType, action: ActionType) -> bool:
        """Verifica si el usuario tiene un permiso específico."""
        # Los administradores tienen todos los permisos
        if self.role == Role.ADMIN:
            return True
        
        # Verificar permisos específicos del usuario
        if self.permissions:
            return self.permissions.has_permission(resource, action)
        
        # Permisos por defecto basados en rol
        return self._get_default_permissions().has_permission(resource, action)
    
    def _get_default_permissions(self) -> PermissionSet:
        """Obtiene los permisos por defecto según el rol."""
        default_permissions = set()
        
        if self.role == Role.ADMIN:
            # Los administradores pueden hacer todo
            default_permissions.add(Permission(
                id="admin_all",
                name="Admin All Access",
                resource=ResourceType.ALL,
                action=ActionType.ALL,
                description="Full admin access"
            ))
        elif self.role == Role.MANAGER:
            # Los managers pueden leer y crear/actualizar productos y proveedores
            default_permissions.update([
                Permission("manager_products_all", "Manager Products", ResourceType.PRODUCTS, ActionType.ALL, "Manage products"),
                Permission("manager_providers_all", "Manager Providers", ResourceType.PROVIDERS, ActionType.ALL, "Manage providers"),
                Permission("manager_users_read", "Manager Users Read", ResourceType.USERS, ActionType.READ, "Read users"),
                Permission("manager_health_read", "Manager Health", ResourceType.HEALTH, ActionType.READ, "Read health status")
            ])
        elif self.role == Role.VIEWER:
            # Los viewers solo pueden leer
            default_permissions.update([
                Permission("viewer_products_read", "Viewer Products", ResourceType.PRODUCTS, ActionType.READ, "Read products"),
                Permission("viewer_providers_read", "Viewer Providers", ResourceType.PROVIDERS, ActionType.READ, "Read providers"),
                Permission("viewer_health_read", "Viewer Health", ResourceType.HEALTH, ActionType.READ, "Read health status")
            ])
        elif self.role == Role.USER:
            # Los usuarios básicos pueden leer productos y proveedores
            default_permissions.update([
                Permission("user_products_read", "User Products", ResourceType.PRODUCTS, ActionType.READ, "Read products"),
                Permission("user_providers_read", "User Providers", ResourceType.PROVIDERS, ActionType.READ, "Read providers")
            ])
        
        return PermissionSet(default_permissions)
    
    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador."""
        return self.role == Role.ADMIN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role.value,
            "is_active": self.is_active,
            "permissions": self.permissions.to_dict() if self.permissions else None
        }