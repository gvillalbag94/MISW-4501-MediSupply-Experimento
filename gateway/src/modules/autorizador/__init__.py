"""
Módulo de Autorización Simplificado.

Funcionalidades principales:
1. Validación de tokens JWT (generados por otro módulo)
2. Validación de acceso por rol (extraído del token)

Componentes:
- TokenValidator: Valida tokens JWT
- AccessValidator: Valida acceso basado en roles
- AuthorizationService: Orquesta ambas funcionalidades
- AuthorizationMiddleware: Intercepta requests automáticamente
"""

# Entidades del dominio
from .dominio.entities.token_payload import TokenPayload, Role
from .dominio.entities.resource import ResourceType, ActionType, AccessRequest, RolePermissions
from .dominio.exceptions import (
    AuthorizationError,
    InvalidTokenError,
    ExpiredTokenError,
    InsufficientPermissionsError,
    MissingTokenError
)

# Casos de uso
from .aplicacion.use_cases.token_validator import TokenValidator
from .aplicacion.use_cases.access_validator import AccessValidator

# Servicios
from .aplicacion.servicios.authorization_service import AuthorizationService

# Infraestructura
from .infraestructura.middleware.authorization_middleware import (
    AuthorizationMiddleware,
    create_authorization_middleware
)


def create_authorization_module(secret_key: str, algorithm: str = "HS256") -> AuthorizationService:
    """
    Factory simplificado para crear el módulo de autorización.
    
    Args:
        secret_key: Clave secreta para validar tokens JWT
        algorithm: Algoritmo JWT
        
    Returns:
        AuthorizationService configurado y listo para usar
    """
    return AuthorizationService(secret_key, algorithm)


# Exportar componentes principales
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
    "MissingTokenError",
    
    # Casos de uso
    "TokenValidator",
    "AccessValidator",
    
    # Servicios
    "AuthorizationService",
    
    # Middleware
    "AuthorizationMiddleware",
    "create_authorization_middleware",
    
    # Factory
    "create_authorization_module"
]