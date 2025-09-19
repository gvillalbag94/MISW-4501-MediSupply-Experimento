"""
Middleware de autorización simplificado.
Intercepta requests y aplica las dos funcionalidades principales.
"""
from flask import Flask, request, jsonify
from typing import Optional
from datetime import datetime

from ...aplicacion.servicios.auth_service import AuthService


class AuthorizationMiddleware:
    """
    Middleware de autorización para Flask.
    
    Funcionalidades:
    1. Intercepta todas las requests automáticamente
    2. Valida tokens JWT
    3. Valida acceso por rol
    4. Permite o rechaza el acceso
    """
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
    
    def before_request(self):
        """
        Función que se ejecuta antes de cada request.
        Implementa la lógica de autorización transparente con validación robusta de tokens.
        """
        route = request.path
        method = request.method
        
        # Skip para métodos OPTIONS (CORS preflight)
        if method == 'OPTIONS':
            return None
        
        # Obtener header de autorización
        authorization_header = request.headers.get('Authorization')
        
        # Log para debugging (sin exponer el token completo)
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Validating access for {method} {route}")
        
        # Autorizar request usando el servicio simplificado (incluye validación de firma)
        authorized = self.auth_service.authorize_access(authorization_header, route, method, request)
        
        if not authorized:
            logger.warning(f"Unauthorized access attempt to {method} {route}")
            return jsonify({
                "error": "No autorizado",
                "message": "Token inválido, expirado, alterado o permisos insuficientes",
                "code": "UNAUTHORIZED",
                "route": route,
                "method": method,
                "timestamp": str(datetime.now()),
                "details": "El token debe ser válido y no haber sido modificado"
            }), 401
        
        # Si está autorizado, continuar con la request
        logger.debug(f"Access granted for {method} {route}")
        return None


def create_authorization_middleware(app: Flask, secret_key: str, algorithm: str = "HS256") -> AuthService:
    """
    Factory para crear y registrar el middleware de autorización.
    Configura validación robusta de tokens JWT con verificación de integridad.
    
    Args:
        app: Aplicación Flask
        secret_key: Clave secreta para validar tokens JWT
        algorithm: Algoritmo JWT (por defecto HS256)
        
    Returns:
        AuthService configurado
        
    Raises:
        ValueError: Si la clave secreta no cumple con los requisitos de seguridad
    """
    # Validaciones de configuración
    if not secret_key or len(secret_key) < 32:
        raise ValueError("La clave secreta debe tener al menos 32 caracteres para seguridad")
    
    # Crear servicio de autorización
    auth_service = AuthService(secret_key, algorithm)
    
    # Crear middleware
    middleware = AuthorizationMiddleware(auth_service)
    
    # Registrar middleware en Flask
    app.before_request(middleware.before_request)
    
    print(f"✅ Middleware de autorización activado")
    print(f"   - Validación de tokens JWT: ✅")
    print(f"   - Verificación de integridad (anti-alteración): ✅")
    print(f"   - Validación de acceso por rol: ✅")
    print(f"   - Algoritmo: {algorithm}")
    print(f"   - Rutas protegidas: /productos")
    print(f"   - Rutas públicas: /, /health, /auth/*")
    
    return auth_service