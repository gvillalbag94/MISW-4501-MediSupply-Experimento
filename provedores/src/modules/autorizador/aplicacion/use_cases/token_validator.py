"""
Use case para validar tokens JWT.
"""
import jwt
from datetime import datetime
from typing import Optional

from ...dominio.entities.token_payload import TokenPayload
from ...dominio.exceptions import InvalidTokenError, ExpiredTokenError


class TokenValidator:
    """
    Caso de uso para validar tokens JWT.
    No genera tokens, solo los valida.
    """
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def validate_token(self, token: str) -> TokenPayload:
        """
        Valida un token JWT y devuelve el payload.
        
        Args:
            token: Token JWT a validar
            
        Returns:
            TokenPayload con la información del token
            
        Raises:
            InvalidTokenError: Si el token es inválido
            ExpiredTokenError: Si el token ha expirado
        """
        try:
            # Decodificar token
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            
            # Crear objeto TokenPayload
            token_payload = TokenPayload.from_dict(payload)
            
            # Verificar expiración
            if token_payload.is_expired():
                raise ExpiredTokenError("El token ha expirado")
            
            return token_payload
            
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError("El token ha expirado")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Token inválido o malformado")
        except (KeyError, ValueError, TypeError) as e:
            raise InvalidTokenError(f"Formato de token inválido: {str(e)}")
    
    def extract_token_from_header(self, authorization_header: Optional[str]) -> Optional[str]:
        """
        Extrae el token del header Authorization.
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            
        Returns:
            Token extraído o None si no está presente
        """
        if not authorization_header:
            return None
        
        # Formato esperado: "Bearer <token>"
        parts = authorization_header.split(' ')
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
        
        return parts[1]
