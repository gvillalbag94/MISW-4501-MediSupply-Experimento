"""
Servicio de autorización simplificado.
Orquesta las dos funcionalidades principales:
1. Validación de tokens
2. Validación de acceso por rol
"""
from typing import Optional, Dict, Tuple

from ..use_cases.token_validator import TokenValidator
from ..use_cases.access_validator import AccessValidator
from ...dominio.entities.token_payload import TokenPayload
from ...dominio.exceptions import (
    MissingTokenError, 
    InvalidTokenError, 
    ExpiredTokenError,
    InsufficientPermissionsError
)


class AuthorizationService:
    """
    Servicio principal de autorización.
    
    Responsabilidades:
    1. Validar tokens JWT (delegando al TokenValidator)
    2. Validar acceso por rol (delegando al AccessValidator)
    """
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.token_validator = TokenValidator(secret_key, algorithm)
        self.access_validator = AccessValidator()
    
    def validate_token(self, authorization_header: Optional[str]) -> TokenPayload:
        """
        Valida un token desde el header Authorization.
        Verifica que el token no haya sido alterado y que sea válido.
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            
        Returns:
            TokenPayload con información del usuario
            
        Raises:
            MissingTokenError: Si no se proporciona token
            InvalidTokenError: Si el token es inválido o ha sido alterado
            ExpiredTokenError: Si el token ha expirado
        """
        if not authorization_header:
            raise MissingTokenError("Header Authorization requerido")
        
        # Extraer token del header
        token = self.token_validator.extract_token_from_header(authorization_header)
        
        if not token:
            raise MissingTokenError("Token de autorización requerido en formato 'Bearer <token>'")
        
        # Validar token (incluye verificación de firma y integridad)
        return self.token_validator.validate_token(token)
    
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
        return self.access_validator.validate_access(token_payload, route, method)
    
    def authorize_request(self, authorization_header: Optional[str], route: str, method: str) -> Tuple[bool, Optional[TokenPayload]]:
        """
        Autoriza una request completa (token + acceso).
        
        Este método combina ambas funcionalidades principales:
        1. Validación de token (incluye verificación de integridad)
        2. Validación de acceso por rol
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            route: Ruta solicitada
            method: Método HTTP
            
        Returns:
            Tupla (autorizado, token_payload)
            - autorizado: True si está autorizado
            - token_payload: Información del token (None si no autorizado)
        """
        try:
            # 0. Verificar si es ruta pública PRIMERO
            if self.access_validator._is_public_route(route):
                return True, None
            
            # 1. Validar token (incluye verificación de firma para prevenir alteración)
            token_payload = self.validate_token(authorization_header)
            
            # 2. Validar acceso por rol
            self.validate_access(token_payload, route, method)
            
            return True, token_payload
            
        except (MissingTokenError, InvalidTokenError, ExpiredTokenError, InsufficientPermissionsError) as e:
            # Log del error para debugging (sin exponer detalles sensibles)
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Autorización denegada para {method} {route}: {type(e).__name__}")
            return False, None
        except Exception as e:
            # Log de errores inesperados
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error inesperado en autorización para {method} {route}: {str(e)}")
            return False, None
    
    def is_public_route(self, route: str) -> bool:
        """
        Verifica si una ruta es pública (no requiere autorización).
        
        Args:
            route: Ruta a verificar
            
        Returns:
            True si es pública
        """
        return self.access_validator._is_public_route(route)
    
    def get_user_info(self, authorization_header: Optional[str]) -> Optional[Dict]:
        """
        Obtiene información del usuario desde el token.
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            
        Returns:
            Diccionario con información del usuario o None si es inválido
        """
        try:
            token_payload = self.validate_token(authorization_header)
            return self.access_validator.get_user_permissions(token_payload)
        except:
            return None
