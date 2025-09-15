from typing import Optional
from ...dominio.entities import ResourceType, ActionType
from ...dominio.exceptions import (
    AuthorizationError, InvalidTokenError, ExpiredTokenError, 
    InsufficientPermissionsError, UserNotFoundError, UserInactiveError,
    TokenNotFoundError
)
from ..use_cases.auth_use_case import AuthUseCase
from ..use_cases.token_validation_use_case import TokenValidationUseCase
from ..use_cases.authorization_use_case import AuthorizationUseCase
from ..dtos.session_dto import SessionDto
from ..dtos.token_dto import AuthorizationRequestDto, AuthorizationResponseDto


class AuthService:
    """
    Servicio de aplicación para autenticación y autorización.
    """
    
    def __init__(
        self, 
        auth_use_case: AuthUseCase,
        token_validation_use_case: TokenValidationUseCase,
        authorization_use_case: AuthorizationUseCase
    ):
        self.auth_use_case = auth_use_case
        self.token_validation_use_case = token_validation_use_case
        self.authorization_use_case = authorization_use_case
    
    def login(self, email: str, password: str) -> Optional[SessionDto]:
        """
        Autentica un usuario y crea una sesión.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            
        Returns:
            SessionDto: DTO de la sesión creada, None si falla
        """
        try:
            return self.auth_use_case.login(email, password)
        except (UserNotFoundError, UserInactiveError) as e:
            # Log the error but return None for security
            print(f"Login failed: {str(e)}")
            return None
    
    def logout(self, token: str) -> bool:
        """
        Cierra la sesión del usuario.
        
        Args:
            token: Token de la sesión
            
        Returns:
            bool: True si se cerró exitosamente
        """
        try:
            return self.auth_use_case.logout(token)
        except Exception as e:
            print(f"Logout failed: {str(e)}")
            return False
    
    def validate_token(self, token: str) -> bool:
        """
        Valida un token de autenticación.
        
        Args:
            token: Token a validar
            
        Returns:
            bool: True si el token es válido
        """
        try:
            self.token_validation_use_case.validate_token(token)
            return True
        except (InvalidTokenError, ExpiredTokenError, UserNotFoundError, AuthorizationError, TokenNotFoundError) as e:
            print(f"Token validation failed: {str(e)}")
            return False
    
    def authorize_request(self, request: AuthorizationRequestDto) -> AuthorizationResponseDto:
        """
        Autoriza una solicitud de acceso.
        
        Args:
            request: Solicitud de autorización
            
        Returns:
            AuthorizationResponseDto: Respuesta de autorización
        """
        try:
            # Convertir strings a enums
            resource = ResourceType(request.resource)
            action = ActionType(request.action)
            
            # Autorizar la solicitud
            user = self.authorization_use_case.authorize_request(
                request.token, resource, action
            )
            
            return AuthorizationResponseDto(
                authorized=True,
                user_id=user.id,
                user_role=user.role.value,
                message="Access granted"
            )
            
        except (InvalidTokenError, ExpiredTokenError) as e:
            return AuthorizationResponseDto(
                authorized=False,
                user_id="",
                user_role="",
                message=f"Token error: {str(e)}"
            )
        except InsufficientPermissionsError as e:
            return AuthorizationResponseDto(
                authorized=False,
                user_id="",
                user_role="",
                message=f"Insufficient permissions: {str(e)}"
            )
        except UserNotFoundError as e:
            return AuthorizationResponseDto(
                authorized=False,
                user_id="",
                user_role="",
                message=f"User error: {str(e)}"
            )
        except ValueError as e:
            return AuthorizationResponseDto(
                authorized=False,
                user_id="",
                user_role="",
                message=f"Invalid resource or action: {str(e)}"
            )
        except Exception as e:
            return AuthorizationResponseDto(
                authorized=False,
                user_id="",
                user_role="",
                message=f"Authorization failed: {str(e)}"
            )
    
    def check_admin_access(self, token: str) -> AuthorizationResponseDto:
        """
        Verifica si el usuario tiene acceso de administrador.
        
        Args:
            token: Token del usuario
            
        Returns:
            AuthorizationResponseDto: Respuesta de autorización
        """
        try:
            user = self.authorization_use_case.authorize_admin_only(token)
            
            return AuthorizationResponseDto(
                authorized=True,
                user_id=user.id,
                user_role=user.role.value,
                message="Admin access granted"
            )
            
        except AuthorizationError as e:
            return AuthorizationResponseDto(
                authorized=False,
                user_id="",
                user_role="",
                message=str(e)
            )