"""
Middleware de autorización simplificado.
Intercepta requests y aplica las dos funcionalidades principales.
"""
from flask import Flask, request, jsonify
from typing import Optional

from ...aplicacion.servicios.authorization_service import AuthorizationService


class AuthorizationMiddleware:
    """
    Middleware de autorización para Flask.
    
    Funcionalidades:
    1. Intercepta todas las requests automáticamente
    2. Valida tokens JWT
    3. Valida acceso por rol
    4. Permite o rechaza el acceso
    """
    
    def __init__(self, authorization_service: AuthorizationService):
        self.authorization_service = authorization_service
    
    def before_request(self):
        """
        Función que se ejecuta antes de cada request.
        Implementa la lógica de autorización transparente.
        """
        route = request.path
        method = request.method
        
        # Verificar si es ruta pública
        if self.authorization_service.is_public_route(route):
            return None  # Permitir acceso
        
        # Obtener header de autorización
        authorization_header = request.headers.get('Authorization')
        
        # Autorizar request
        authorized, token_payload = self.authorization_service.authorize_request(
            authorization_header, route, method
        )
        
        if not authorized:
            return jsonify({
                "error": "No autorizado",
                "message": "Token inválido o permisos insuficientes",
                "code": "UNAUTHORIZED",
                "route": route,
                "method": method
            }), 401
        
        # Si está autorizado, continuar con la request
        return None


def create_authorization_middleware(app: Flask, secret_key: str, algorithm: str = "HS256") -> AuthorizationService:
    """
    Factory para crear y registrar el middleware de autorización.
    
    Args:
        app: Aplicación Flask
        secret_key: Clave secreta para validar tokens JWT
        algorithm: Algoritmo JWT (por defecto HS256)
        
    Returns:
        AuthorizationService configurado
    """
    # Crear servicio de autorización
    authorization_service = AuthorizationService(secret_key, algorithm)
    
    # Crear middleware
    middleware = AuthorizationMiddleware(authorization_service)
    
    # Registrar middleware en Flask
    app.before_request(middleware.before_request)
    
    print(f"✅ Middleware de autorización activado")
    print(f"   - Validación de tokens: ✅")
    print(f"   - Validación de acceso por rol: ✅")
    print(f"   - Rutas protegidas: /productos, /provedores, /users")
    print(f"   - Rutas públicas: /, /health, /auth/*")
    
    return authorization_service
