from typing import Optional
from ..use_cases.token_validator import TokenValidator
from ..use_cases.access_validator import AccessValidator
from ...dominio.entities.token_payload import TokenPayload
from ...dominio.exceptions import (
    MissingTokenError, InvalidTokenError, ExpiredTokenError,
    InsufficientPermissionsError
)


class AuthService:
    """
    Servicio de aplicación simplificado para validación de tokens en microservicios.
    Solo maneja validación de tokens JWT, no autenticación completa.
    """
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.token_validator = TokenValidator(secret_key, algorithm)
        self.access_validator = AccessValidator()
    
    def validate_token(self, authorization_header: Optional[str]) -> bool:
        """
        Valida un token de autenticación desde el header Authorization.
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            
        Returns:
            bool: True si el token es válido
        """
        try:
            # Extraer token del header
            token = self.token_validator.extract_token_from_header(authorization_header)
            
            if not token:
                return False
            
            # Validar token
            self.token_validator.validate_token(token)
            return True
            
        except (InvalidTokenError, ExpiredTokenError, MissingTokenError) as e:
            print(f"Token validation failed: {str(e)}")
            return False
    
    def get_token_payload(self, authorization_header: Optional[str]) -> Optional[TokenPayload]:
        """
        Obtiene el payload del token si es válido.
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            
        Returns:
            TokenPayload si es válido, None si no
        """
        try:
            # Extraer token del header
            token = self.token_validator.extract_token_from_header(authorization_header)
            
            if not token:
                return None
            
            # Validar y obtener payload
            return self.token_validator.validate_token(token)
            
        except (InvalidTokenError, ExpiredTokenError, MissingTokenError):
            return None
    
    def authorize_access(self, authorization_header: Optional[str], route: str, method: str, request=None) -> bool:
        """
        Autoriza acceso a una ruta específica.
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            route: Ruta solicitada
            method: Método HTTP
            request: Objeto request de Flask (opcional)
            
        Returns:
            bool: True si el acceso está autorizado
        """
        try:
            # Verificar si es ruta pública primero
            if self.access_validator._is_public_route(route):
                return True
            
            # Verificar si es petición interna (del Gateway)
            if request and self.access_validator._is_internal_request(request):
                # Para peticiones internas, permitir acceso si es de red interna
                # Esto permite que el Gateway acceda sin token cuando valida internamente
                return True
            
            # Obtener payload del token
            token_payload = self.get_token_payload(authorization_header)
            
            if not token_payload:
                return False
            
            # Validar acceso por rol
            self.access_validator.validate_access(token_payload, route, method)
            return True
            
        except (InsufficientPermissionsError, Exception):
            return False
    
    def get_user_info(self, authorization_header: Optional[str]) -> Optional[dict]:
        """
        Obtiene información del usuario desde el token.
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            
        Returns:
            Diccionario con información del usuario o None si es inválido
        """
        token_payload = self.get_token_payload(authorization_header)
        
        if not token_payload:
            return None
        
        return self.access_validator.get_user_permissions(token_payload)