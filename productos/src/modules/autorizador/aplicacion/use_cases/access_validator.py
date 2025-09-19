"""
Use case para validar acceso basado en roles.
"""
from typing import Dict, Tuple

from ...dominio.entities.token_payload import TokenPayload, Role
from ...dominio.entities.resource import ResourceType, ActionType, AccessRequest, RolePermissions
from ...dominio.exceptions import InsufficientPermissionsError


class AccessValidator:
    """
    Caso de uso para validar acceso basado en roles del token.
    """
    
    def __init__(self):
        # Mapeo de rutas a recursos y acciones (solo para productos)
        self.route_permissions: Dict[str, Dict[str, Tuple[ResourceType, ActionType]]] = {
            "/productos": {
                "GET": (ResourceType.PRODUCTS, ActionType.READ),
                "POST": (ResourceType.PRODUCTS, ActionType.CREATE),
                "PUT": (ResourceType.PRODUCTS, ActionType.UPDATE),
                "DELETE": (ResourceType.PRODUCTS, ActionType.DELETE)
            }
        }
        
        # Rutas que no requieren autorización (específicas para productos)
        self.public_routes = {
            "/",
            "/health",
            "/auth/resources"  # Para que el Gateway pueda consultar recursos
        }
    
    def validate_access(self, token_payload: TokenPayload, route: str, method: str) -> bool:
        """
        Valida si el usuario puede acceder a una ruta específica.
        
        Args:
            token_payload: Información del token validado
            route: Ruta solicitada (ej: "/productos")
            method: Método HTTP (ej: "GET")
            
        Returns:
            True si el acceso está permitido
            
        Raises:
            InsufficientPermissionsError: Si no tiene permisos
        """
        # Verificar si es ruta pública
        if self._is_public_route(route):
            return True
        
        # Obtener recurso y acción requerida
        resource, action = self._get_required_permission(route, method)
        
        # Crear solicitud de acceso
        access_request = AccessRequest(
            resource=resource,
            action=action,
            user_role=token_payload.role
        )
        
        # Validar permisos
        if not RolePermissions.can_access(token_payload.role, resource, action):
            raise InsufficientPermissionsError(
                f"Usuario con rol '{token_payload.role.value}' no puede realizar "
                f"'{action.value}' en '{resource.value}'"
            )
        
        return True
    
    def _is_public_route(self, route: str) -> bool:
        """Verifica si una ruta es pública."""
        # Verificar rutas exactas
        if route in self.public_routes:
            return True
        
        # Verificar prefijos públicos
        public_prefixes = ["/health", "/auth/"]
        return any(route.startswith(prefix) for prefix in public_prefixes)
    
    def _is_internal_request(self, request) -> bool:
        """
        Verifica si la petición viene del Gateway interno.
        IMPORTANTE: Solo permitir bypass de auth para peticiones explícitamente marcadas como internas.
        NO permitir bypass solo por IP para evitar vulnerabilidades de seguridad.
        """
        # Verificar headers internos del Gateway (debe ser explícito)
        internal_header = request.headers.get('X-Internal-Request')
        gateway_token = request.headers.get('X-Gateway-Token')
        
        # Solo permitir bypass si hay headers específicos de gateway interno
        # NO permitir bypass solo por IP de red interna (vulnerabilidad de seguridad)
        return (internal_header == 'true' and gateway_token is not None)
    
    def _get_required_permission(self, route: str, method: str) -> Tuple[ResourceType, ActionType]:
        """
        Obtiene el recurso y acción requerida para una ruta y método.
        
        Returns:
            Tupla (ResourceType, ActionType)
            
        Raises:
            InsufficientPermissionsError: Si la ruta no está mapeada
        """
        # Buscar ruta exacta
        if route in self.route_permissions:
            method_permissions = self.route_permissions[route]
            if method in method_permissions:
                return method_permissions[method]
        
        # Buscar por prefijo de ruta
        for route_pattern, methods in self.route_permissions.items():
            if route.startswith(route_pattern):
                if method in methods:
                    return methods[method]
        
        # Si no se encuentra, denegar acceso
        raise InsufficientPermissionsError(f"Ruta no autorizada: {method} {route}")
    
    def get_user_permissions(self, token_payload: TokenPayload) -> Dict[str, list]:
        """
        Obtiene todos los permisos del usuario basado en su rol.
        
        Args:
            token_payload: Información del token validado
            
        Returns:
            Diccionario con permisos del usuario
        """
        permissions = RolePermissions.PERMISSIONS.get(token_payload.role, {})
        
        formatted_permissions = {}
        for resource, actions in permissions.items():
            formatted_permissions[resource.value] = [action.value for action in actions]
        
        return {
            "role": token_payload.role.value,
            "permissions": formatted_permissions,
            "user_id": token_payload.user_id
        }
