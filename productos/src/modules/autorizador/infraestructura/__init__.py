"""
Infraestructura del módulo de autorización refactorizado.
"""

from .middleware.authorization_middleware import (
    AuthorizationMiddleware,
    create_authorization_middleware
)

__all__ = [
    "AuthorizationMiddleware",
    "create_authorization_middleware"
]
