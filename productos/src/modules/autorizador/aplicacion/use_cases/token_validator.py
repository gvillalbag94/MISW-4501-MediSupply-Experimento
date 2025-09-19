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
        Verifica la integridad del token (que no haya sido alterado) y su validez.
        
        Args:
            token: Token JWT a validar
            
        Returns:
            TokenPayload con la información del token
            
        Raises:
            InvalidTokenError: Si el token es inválido o ha sido alterado
            ExpiredTokenError: Si el token ha expirado
        """
        if not token or not isinstance(token, str):
            raise InvalidTokenError("Token debe ser una cadena no vacía")
        
        try:
            # Decodificar y verificar token
            # jwt.decode automáticamente verifica la firma usando la secret_key
            # Si el token ha sido alterado, fallará la verificación de firma
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                options={
                    "verify_signature": True,  # Verificar firma (previene alteración)
                    "verify_exp": True,       # Verificar expiración
                    "require": ["user_id", "role", "exp"]  # Campos requeridos
                }
            )
            
            # Validaciones adicionales del payload
            self._validate_payload_structure(payload)
            
            # Crear objeto TokenPayload
            token_payload = TokenPayload.from_dict(payload)
            
            # Verificación adicional de expiración (doble check)
            if token_payload.is_expired():
                raise ExpiredTokenError("El token ha expirado")
            
            return token_payload
            
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError("El token ha expirado")
        except jwt.InvalidSignatureError:
            raise InvalidTokenError("Token ha sido alterado o firma inválida")
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(f"Token inválido: {str(e)}")
        except (KeyError, ValueError, TypeError) as e:
            raise InvalidTokenError(f"Formato de token inválido: {str(e)}")
        except Exception as e:
            raise InvalidTokenError(f"Error al validar token: {str(e)}")
    
    def extract_token_from_header(self, authorization_header: Optional[str]) -> Optional[str]:
        """
        Extrae el token del header Authorization.
        
        Args:
            authorization_header: Header 'Authorization: Bearer <token>'
            
        Returns:
            Token extraído o None si no está presente
            
        Raises:
            InvalidTokenError: Si el header está malformado
        """
        if not authorization_header or not isinstance(authorization_header, str):
            return None
        
        # Formato esperado: "Bearer <token>"
        parts = authorization_header.strip().split(' ')
        
        # Validar que tenga exactamente 2 partes
        if len(parts) != 2:
            if authorization_header.strip().lower().startswith('bearer'):
                # Header malformado: "Bearer" sin token
                raise InvalidTokenError("Header Authorization malformado: falta el token después de 'Bearer'")
            return None
        
        if parts[0].lower() != 'bearer':
            return None
        
        token = parts[1].strip()
        
        # Validaciones básicas del token
        if not token or len(token) < 10:  # JWT mínimo tiene más de 10 caracteres
            raise InvalidTokenError("Token vacío o demasiado corto")
        
        # Verificar que tenga estructura JWT básica (3 partes separadas por .)
        token_parts = token.split('.')
        if len(token_parts) != 3:
            raise InvalidTokenError("Token no tiene formato JWT válido (debe tener 3 partes separadas por '.')")
        
        return token
    
    def _validate_payload_structure(self, payload: dict) -> None:
        """
        Valida la estructura del payload del token.
        
        Args:
            payload: Diccionario con el payload del token
            
        Raises:
            InvalidTokenError: Si la estructura no es válida
        """
        required_fields = ["user_id", "role", "exp"]
        
        # Verificar campos requeridos
        for field in required_fields:
            if field not in payload:
                raise InvalidTokenError(f"Campo requerido '{field}' no encontrado en el token")
        
        # Validar tipos de datos
        if not isinstance(payload["user_id"], (str, int)):
            raise InvalidTokenError("user_id debe ser string o número")
        
        if not isinstance(payload["role"], str):
            raise InvalidTokenError("role debe ser string")
        
        if not isinstance(payload["exp"], (int, float)):
            raise InvalidTokenError("exp debe ser timestamp numérico")
        
        # Validar que el role sea válido
        valid_roles = ["admin", "manager", "user", "viewer"]
        if payload["role"] not in valid_roles:
            raise InvalidTokenError(f"Rol '{payload['role']}' no es válido")