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
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            
        Returns:
            TokenPayload con información del usuario
            
        Raises:
            MissingTokenError: Si no se proporciona token
            InvalidTokenError: Si el token es inválido
            ExpiredTokenError: Si el token ha expirado
        """
        # Extraer token del header
        token = self.token_validator.extract_token_from_header(authorization_header)
        
        if not token:
            raise MissingTokenError("Token de autorización requerido")
        
        # Validar token
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
        1. Validación de token
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
            # 1. Validar token
            token_payload = self.validate_token(authorization_header)
            
            # 2. Validar acceso por rol
            self.validate_access(token_payload, route, method)
            
            return True, token_payload
            
        except (MissingTokenError, InvalidTokenError, ExpiredTokenError, InsufficientPermissionsError):
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
