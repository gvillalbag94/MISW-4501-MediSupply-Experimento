"""
Middleware de autorización simplificado para microservicios.

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

logger = logging.getLogger(__name__)


class AuthMiddleware:
    """
    Middleware de autorización simplificado para validar tokens y permisos.
    """
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
    
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
            # Obtener header de autorización
            auth_header = request.headers.get('Authorization')
            
            # Autorizar usando el servicio simplificado
            authorized = self.auth_service.authorize_access(auth_header, path, method)
            
            if authorized:
                # Si está autorizado, obtener info del usuario para almacenar en g
                user_info = self.auth_service.get_user_info(auth_header)
                if user_info:
                    g.current_user_id = user_info.get('user_id', '')
                    g.current_user_role = user_info.get('role', '')
                    g.current_user_permissions = user_info.get('permissions', {})
                
                logger.debug(f"Autorización exitosa para {method} {path}")
                return True, {}
            else:
                logger.warning(f"Autorización denegada para {method} {path}")
                return False, {
                    "error": "Acceso denegado",
                    "message": "Token inválido o permisos insuficientes"
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
