"""
Middleware de autorización para el Gateway.

Este middleware intercepta las solicitudes HTTP y valida:
1. Token de autenticación en headers
2. Permisos del usuario para acceder al recurso solicitado
3. Manejo de errores de autorización
"""

import logging
from functools import wraps
from typing import Dict, Any, Tuple, Optional
from flask import request, jsonify, g

from ...aplicacion.servicios.auth_service import AuthService
from ...aplicacion.dtos.token_dto import AuthorizationRequestDto
from ...dominio.entities import ResourceType, ActionType
from ...dominio.exceptions import (
    AuthorizationError, InvalidTokenError, ExpiredTokenError,
    InsufficientPermissionsError, UserNotFoundError, UserInactiveError
)
from ...config import AuthConfig, RouteConfig

logger = logging.getLogger(__name__)


class AuthMiddleware:
    """
    Middleware de autorización para validar tokens y permisos.
    """
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
    
    def extract_token_from_header(self, authorization_header: str) -> Optional[str]:
        """
        Extrae el token del header Authorization.
        
        Args:
            authorization_header: Header Authorization
            
        Returns:
            str: Token extraído o None si no es válido
        """
        if not authorization_header:
            return None
        
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
        
        return parts[1]
    
    def get_resource_and_action(self, path: str, method: str) -> Optional[Tuple[ResourceType, ActionType]]:
        """
        Obtiene el recurso y acción para una ruta y método específicos.
        
        Args:
            path: Ruta de la solicitud
            method: Método HTTP
            
        Returns:
            Tuple[ResourceType, ActionType]: Recurso y acción o None si no requiere auth
        """
        return AuthConfig.get_required_permission(path, method)
    
    def is_public_route(self, path: str) -> bool:
        """
        Verifica si una ruta es pública (no requiere autenticación).
        
        Args:
            path: Ruta de la solicitud
            
        Returns:
            bool: True si es ruta pública
        """
        return AuthConfig.is_public_route(path)
    
    def validate_request(self, path: str, method: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Valida una solicitud HTTP.
        
        Args:
            path: Ruta de la solicitud
            method: Método HTTP
            
        Returns:
            Tuple[bool, Dict]: (es_válida, response_data)
        """
        try:
            # Verificar si es ruta pública
            if self.is_public_route(path):
                logger.debug(f"Ruta pública permitida: {method} {path}")
                return True, {}
            
            # Obtener token del header
            auth_header = request.headers.get('Authorization')
            token = self.extract_token_from_header(auth_header)
            
            if not token:
                logger.warning(f"Token requerido para: {method} {path}")
                return False, {
                    "error": "Token de autorización requerido",
                    "message": "Debe incluir 'Authorization: Bearer <token>' en los headers"
                }
            
            # Obtener recurso y acción para la ruta
            resource_action = self.get_resource_and_action(path, method)
            
            if not resource_action:
                logger.warning(f"Ruta no configurada para autorización: {method} {path}")
                return False, {
                    "error": "Ruta no autorizada",
                    "message": f"La ruta {path} no está configurada para autorización"
                }
            
            resource, action = resource_action
            
            # Crear solicitud de autorización
            auth_request = AuthorizationRequestDto(
                token=token,
                resource=resource.value,
                action=action.value
            )
            
            # Validar autorización
            auth_response = self.auth_service.authorize_request(auth_request)
            
            if auth_response.authorized:
                # Almacenar información del usuario en g para uso posterior
                g.current_user_id = auth_response.user_id
                g.current_user_role = auth_response.user_role
                g.current_token = token
                
                logger.info(f"Autorización exitosa: {auth_response.user_role} usuario {auth_response.user_id} accediendo a {method} {path}")
                return True, {}
            else:
                logger.warning(f"Autorización denegada: {auth_response.message} para {method} {path}")
                return False, {
                    "error": "Acceso denegado",
                    "message": auth_response.message
                }
                
        except Exception as e:
            logger.error(f"Error en validación de autorización: {str(e)}")
            return False, {
                "error": "Error de autorización",
                "message": "Error interno del servidor al validar autorización"
            }


def require_auth(auth_service: AuthService):
    """
    Decorador para proteger rutas que requieren autenticación y autorización.
    
    Args:
        auth_service: Servicio de autorización
        
    Usage:
        @require_auth(auth_service)
        def mi_endpoint():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            middleware = AuthMiddleware(auth_service)
            
            # Validar la solicitud
            is_valid, error_response = middleware.validate_request(
                request.path, 
                request.method
            )
            
            if not is_valid:
                return jsonify(error_response), 401
            
            # Si es válida, continuar con la función original
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def create_flask_middleware(app, auth_service: AuthService):
    """
    Crea un middleware de Flask que se ejecuta antes de cada solicitud.
    
    Args:
        app: Aplicación Flask
        auth_service: Servicio de autorización
    """
    middleware = AuthMiddleware(auth_service)
    
    @app.before_request
    def before_request():
        """Middleware que se ejecuta antes de cada solicitud."""
        
        # Skip para métodos OPTIONS (CORS preflight)
        if request.method == 'OPTIONS':
            return None
        
        # Validar la solicitud
        is_valid, error_response = middleware.validate_request(
            request.path,
            request.method
        )
        
        if not is_valid:
            return jsonify(error_response), 401
        
        # Si es válida, continuar
        return None
