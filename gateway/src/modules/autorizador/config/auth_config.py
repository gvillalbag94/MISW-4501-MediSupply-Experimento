"""
Configuración de autorización para el Gateway.

Este archivo contiene la configuración de permisos, rutas protegidas,
y políticas de autorización del sistema.
"""

from enum import Enum
from typing import Dict, List, Set, Tuple, Optional
from ..dominio.entities import ResourceType, ActionType, Role


class AuthConfig:
    """
    Configuración centralizada de autorización.
    """
    
    # Rutas que no requieren autenticación
    PUBLIC_ROUTES: Set[str] = {
        "/",
        "/health",
        "/auth/login",
        "/auth/logout", 
        "/auth/resources"
    }
    
    # Prefijos de rutas públicas
    PUBLIC_ROUTE_PREFIXES: List[str] = [
        "/health",
        "/auth/"
    ]
    
    # Mapeo de rutas a recursos y acciones requeridas
    ROUTE_PERMISSIONS: Dict[str, Dict[str, Tuple[ResourceType, ActionType]]] = {
        # Productos
        "/productos": {
            "GET": (ResourceType.PRODUCTS, ActionType.READ),
            "POST": (ResourceType.PRODUCTS, ActionType.CREATE),
            "PUT": (ResourceType.PRODUCTS, ActionType.UPDATE),
            "DELETE": (ResourceType.PRODUCTS, ActionType.DELETE)
        },
        # Proveedores  
        "/provedores": {
            "GET": (ResourceType.PROVIDERS, ActionType.READ),
            "POST": (ResourceType.PROVIDERS, ActionType.CREATE),
            "PUT": (ResourceType.PROVIDERS, ActionType.UPDATE),
            "DELETE": (ResourceType.PROVIDERS, ActionType.DELETE)
        }
    }
    
    # Configuración de permisos por rol (desde las entidades)
    ROLE_PERMISSIONS = {
        Role.ADMIN: "All permissions (*/*)",
        Role.MANAGER: {
            ResourceType.PRODUCTS: [ActionType.CREATE, ActionType.READ, ActionType.UPDATE, ActionType.DELETE],
            ResourceType.PROVIDERS: [ActionType.CREATE, ActionType.READ, ActionType.UPDATE, ActionType.DELETE],
            ResourceType.USERS: [ActionType.READ],
            ResourceType.HEALTH: [ActionType.READ]
        },
        Role.USER: {
            ResourceType.PRODUCTS: [ActionType.READ],
            ResourceType.PROVIDERS: [ActionType.READ]
        },
        Role.VIEWER: {
            ResourceType.PRODUCTS: [ActionType.READ],
            ResourceType.PROVIDERS: [ActionType.READ],
            ResourceType.HEALTH: [ActionType.READ]
        }
    }
    
    # Configuración de tokens
    TOKEN_CONFIG = {
        "expiration_hours": 24,
        "refresh_expiration_days": 7,
        "algorithm": "HS256",
        "issuer": "medisupply-gateway"
    }
    
    # Configuración de seguridad
    SECURITY_CONFIG = {
        "require_https": False,  # Cambiar a True en producción
        "max_failed_attempts": 5,
        "lockout_duration_minutes": 15,
        "password_min_length": 8,
        "require_special_chars": True
    }
    
    @staticmethod
    def is_public_route(path: str) -> bool:
        """
        Verifica si una ruta es pública.
        
        Args:
            path: Ruta a verificar
            
        Returns:
            bool: True si es pública
        """
        # Verificar rutas exactas
        if path in AuthConfig.PUBLIC_ROUTES:
            return True
        
        # Verificar prefijos
        return any(path.startswith(prefix) for prefix in AuthConfig.PUBLIC_ROUTE_PREFIXES)
    
    @staticmethod
    def get_required_permission(path: str, method: str) -> Optional[Tuple[ResourceType, ActionType]]:
        """
        Obtiene el permiso requerido para una ruta y método.
        
        Args:
            path: Ruta de la solicitud
            method: Método HTTP
            
        Returns:
            Tuple[ResourceType, ActionType]: Permiso requerido o None
        """
        # Buscar coincidencia exacta
        if path in AuthConfig.ROUTE_PERMISSIONS:
            permissions = AuthConfig.ROUTE_PERMISSIONS[path]
            return permissions.get(method.upper())
        
        # Buscar por prefijo para rutas con parámetros
        for route_pattern, permissions in AuthConfig.ROUTE_PERMISSIONS.items():
            if path.startswith(route_pattern):
                return permissions.get(method.upper())
        
        return None
    
    @staticmethod
    def get_microservice_from_path(path: str) -> Optional[str]:
        """
        Determina qué microservicio maneja una ruta específica.
        
        Args:
            path: Ruta de la solicitud
            
        Returns:
            str: Nombre del microservicio o None
        """
        if path.startswith("/productos"):
            return "productos"
        elif path.startswith("/provedores"):
            return "provedores"
        elif path.startswith("/health"):
            return "health"
        elif path.startswith("/autorizador"):
            return "authorization"
        
        return None
    
    @staticmethod
    def get_allowed_roles_for_resource(resource: ResourceType, action: ActionType) -> List[Role]:
        """
        Obtiene los roles que tienen permiso para un recurso y acción específicos.
        
        Args:
            resource: Recurso a verificar
            action: Acción a verificar
            
        Returns:
            List[Role]: Lista de roles con permiso
        """
        allowed_roles = []
        
        for role, permissions in AuthConfig.ROLE_PERMISSIONS.items():
            if role == Role.ADMIN:
                # Los administradores tienen todos los permisos
                allowed_roles.append(role)
            elif isinstance(permissions, dict):
                if resource in permissions and action in permissions[resource]:
                    allowed_roles.append(role)
        
        return allowed_roles


class RouteConfig:
    """
    Configuración específica por ruta para casos especiales.
    """
    
    # Rutas que requieren permisos especiales
    ADMIN_ONLY_ROUTES = {
        "/users",
        "/auth/admin-check"
    }
    
    # Rutas con rate limiting especial
    RATE_LIMITED_ROUTES = {
        "/auth/login": {"requests": 5, "window": 60},  # 5 intentos por minuto
        "/productos/buscar": {"requests": 100, "window": 60},  # 100 búsquedas por minuto
        "/provedores/buscar": {"requests": 100, "window": 60}
    }
    
    # Rutas que requieren logging especial
    AUDIT_ROUTES = {
        "/productos": ["POST", "PUT", "DELETE"],
        "/provedores": ["POST", "PUT", "DELETE"],
        "/users": ["POST", "PUT", "DELETE"]
    }
    
    @staticmethod
    def requires_admin(path: str) -> bool:
        """Verifica si una ruta requiere permisos de administrador."""
        return any(path.startswith(admin_route) for admin_route in RouteConfig.ADMIN_ONLY_ROUTES)
    
    @staticmethod
    def requires_audit(path: str, method: str) -> bool:
        """Verifica si una ruta requiere auditoría."""
        for audit_path, methods in RouteConfig.AUDIT_ROUTES.items():
            if path.startswith(audit_path) and method.upper() in methods:
                return True
        return False
