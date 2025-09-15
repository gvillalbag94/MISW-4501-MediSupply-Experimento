from flask import Response, jsonify, request
from ...aplicacion.servicios.auth_service import AuthService
from ...aplicacion.dtos.token_dto import AuthorizationRequestDto
from ...aplicacion.mappers.session_mapper import SessionMapper


class AuthCmd:
    """Controlador para operaciones de autenticación y autorización."""
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def login(self, email: str, password: str) -> Response:
        """Endpoint para iniciar sesión."""
        try:
            session = self.auth_service.login(email, password)
            if session:
                return jsonify(SessionMapper.dto_to_json(session)), 200
            else:
                return jsonify({"error": "Credenciales inválidas"}), 401
        except Exception as e:
            return jsonify({"error": "Error al iniciar sesión"}), 500
    
    def logout(self) -> Response:
        """Endpoint para cerrar sesión."""
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Token requerido"}), 401
            
            token = auth_header.split(' ')[1]
            success = self.auth_service.logout(token)
            
            if success:
                return jsonify({"message": "Sesión cerrada exitosamente"}), 200
            else:
                return jsonify({"error": "Error al cerrar sesión"}), 400
        except Exception as e:
            return jsonify({"error": "Error al cerrar sesión"}), 500
    
    def validate_token(self) -> Response:
        """Endpoint para validar un token."""
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Token requerido"}), 401
            
            token = auth_header.split(' ')[1]
            is_valid = self.auth_service.validate_token(token)
            
            if is_valid:
                return jsonify({"valid": True, "message": "Token válido"}), 200
            else:
                return jsonify({"valid": False, "message": "Token inválido"}), 401
        except Exception as e:
            return jsonify({"error": "Error al validar token"}), 500
    
    def authorize(self) -> Response:
        """Endpoint para autorizar acceso a recursos."""
        try:
            # Obtener datos de la solicitud
            data = request.get_json()
            if not data:
                return jsonify({"error": "Datos requeridos"}), 400
            
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Token requerido"}), 401
            
            token = auth_header.split(' ')[1]
            resource = data.get('resource')
            action = data.get('action')
            
            if not resource or not action:
                return jsonify({"error": "Recurso y acción requeridos"}), 400
            
            # Crear solicitud de autorización
            auth_request = AuthorizationRequestDto(
                token=token,
                resource=resource,
                action=action
            )
            
            # Procesar autorización
            auth_response = self.auth_service.authorize_request(auth_request)
            
            if auth_response.authorized:
                return jsonify({
                    "authorized": True,
                    "user_id": auth_response.user_id,
                    "user_role": auth_response.user_role,
                    "message": auth_response.message
                }), 200
            else:
                return jsonify({
                    "authorized": False,
                    "message": auth_response.message
                }), 403
                
        except Exception as e:
            return jsonify({"error": f"Error en autorización: {str(e)}"}), 500
    
    def check_admin(self) -> Response:
        """Endpoint para verificar acceso de administrador."""
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Token requerido"}), 401
            
            token = auth_header.split(' ')[1]
            auth_response = self.auth_service.check_admin_access(token)
            
            if auth_response.authorized:
                return jsonify({
                    "authorized": True,
                    "user_id": auth_response.user_id,
                    "user_role": auth_response.user_role,
                    "message": auth_response.message
                }), 200
            else:
                return jsonify({
                    "authorized": False,
                    "message": auth_response.message
                }), 403
                
        except Exception as e:
            return jsonify({"error": f"Error en verificación de admin: {str(e)}"}), 500