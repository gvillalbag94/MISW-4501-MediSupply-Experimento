from flask import Response, jsonify, request
from ...aplicacion.servicios.auth_service import AuthService


class AuthCmd:
    """Controlador simplificado para operaciones de validación de tokens en microservicios."""
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def validate_token(self) -> Response:
        """Endpoint para validar un token."""
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Token requerido"}), 401
            
            is_valid = self.auth_service.validate_token(auth_header)
            
            if is_valid:
                return jsonify({"valid": True, "message": "Token válido"}), 200
            else:
                return jsonify({"valid": False, "message": "Token inválido"}), 401
        except Exception as e:
            return jsonify({"error": "Error al validar token"}), 500
    
    def authorize_access(self) -> Response:
        """Endpoint para verificar autorización de acceso a rutas."""
        try:
            # Obtener datos de la solicitud
            data = request.get_json()
            if not data:
                return jsonify({"error": "Datos requeridos"}), 400
            
            auth_header = request.headers.get('Authorization')
            route = data.get('route', '/')
            method = data.get('method', 'GET')
            
            # Verificar autorización
            authorized = self.auth_service.authorize_access(auth_header, route, method)
            
            if authorized:
                user_info = self.auth_service.get_user_info(auth_header)
                return jsonify({
                    "authorized": True,
                    "user_info": user_info,
                    "message": "Acceso autorizado"
                }), 200
            else:
                return jsonify({
                    "authorized": False,
                    "message": "Acceso denegado"
                }), 403
                
        except Exception as e:
            return jsonify({"error": f"Error en autorización: {str(e)}"}), 500
    
    def get_user_info(self) -> Response:
        """Endpoint para obtener información del usuario desde el token."""
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Token requerido"}), 401
            
            user_info = self.auth_service.get_user_info(auth_header)
            
            if user_info:
                return jsonify({
                    "user_info": user_info,
                    "message": "Información obtenida exitosamente"
                }), 200
            else:
                return jsonify({
                    "error": "Token inválido o usuario no encontrado"
                }), 401
                
        except Exception as e:
            return jsonify({"error": f"Error al obtener información del usuario: {str(e)}"}), 500