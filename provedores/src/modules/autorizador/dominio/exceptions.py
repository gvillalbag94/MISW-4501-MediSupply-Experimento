"""
Excepciones específicas del módulo de autorización.
"""


class AuthorizationError(Exception):
    """Excepción base para errores de autorización."""
    pass


class InvalidTokenError(AuthorizationError):
    """Token inválido o malformado."""
    def __init__(self, message: str = "Token inválido"):
        super().__init__(message)


class ExpiredTokenError(AuthorizationError):
    """Token expirado."""
    def __init__(self, message: str = "Token expirado"):
        super().__init__(message)


class InsufficientPermissionsError(AuthorizationError):
    """Usuario no tiene permisos suficientes."""
    def __init__(self, message: str = "Permisos insuficientes"):
        super().__init__(message)


class MissingTokenError(AuthorizationError):
    """Token no proporcionado."""
    def __init__(self, message: str = "Token requerido"):
        super().__init__(message)