import os
from dotenv import load_dotenv
from flask import Flask, g, request
from datetime import datetime
import logging

from src.infraestructura.cmd.provedor_cmd import ProvedorCmd
from src.aplicacion.servicios.provedor_service import ProvedorService
from src.infraestructura.repositorios.provedor_repository import ProvedorRepositoryImpl
from src.aplicacion.use_cases.provedor_use_case import ProvedorUseCase
from src.infraestructura.rutas.provedor_routes import create_provedor_routes

# Módulo de autorización
from src.modules.autorizador import create_authorization_module, create_authorization_middleware

load_dotenv(".env")


class Config:
    """
    Configuración y factory para la aplicación Flask.
    Maneja la inyección de dependencias siguiendo los principios de arquitectura hexagonal.
    """
    
    def __init__(self):
        self.app = None
    
    def create_app(self) -> Flask:
        """
        Crea y configura la aplicación Flask con todas las dependencias.
        
        Returns:
            Flask: Aplicación Flask configurada
        """
        self.app = Flask(__name__)
        
        # Configuración básica
        self._configure_app()
        
        # Configurar logging de requests
        self._configure_request_logging()
        
        # Inyección de dependencias
        self._setup_dependencies()
        
        # Registrar rutas
        self._register_routes()
        
        return self.app
    
    def _configure_app(self):
        """Configura parámetros básicos de la aplicación."""
        self.app.config["ENV"] = os.getenv("ENV", "development")
        self.app.config["DEBUG"] = os.getenv("DEBUG", "False").lower() == "true"
        self.app.config["HOST"] = os.getenv("HOST", "0.0.0.0")
        self.app.config["PORT"] = int(os.getenv("PORT", 5003))
        self.app.config["LOG_LEVEL"] = os.getenv("LOG_LEVEL", "INFO")
        
        # Configuración JWT para autorización
        self.app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "your-secret-key-here")
        self.app.config["ALGORITHM"] = os.getenv("ALGORITHM", "HS256")
    
    def _configure_request_logging(self):
        """Configura el middleware para logging de requests y responses."""
        logger = logging.getLogger("request_logger")
        
        @self.app.before_request
        def log_request():
            """Log cuando entra una petición."""
            g.start_time = datetime.now().time()
            logger.info(f"INCOMING REQUEST: {request.method} {request.url}")
            
            # Log headers si está en modo debug
            if self.app.config.get("DEBUG"):
                logger.debug(f"Headers: {dict(request.headers)}")
                if request.is_json:
                    logger.debug(f"Request Body: {request.get_json()}")
        
        @self.app.after_request
        def log_response(response):
            """Log cuando sale una respuesta."""
            if hasattr(g, "start_time"):
                duration = (datetime.now() - datetime.combine(datetime.today(), g.start_time)).total_seconds()
                logger.info(f"OUTGOING RESPONSE: {response.status_code} - Duration: {duration * 1000:.0f}ms - Size: {len(response.get_data())} bytes")
            else:
                logger.info(f"OUTGOING RESPONSE: {response.status_code}")
            return response
    
    def _setup_dependencies(self):
        """Configura la inyección de dependencias siguiendo arquitectura hexagonal."""
        # Capa de Infraestructura
        provedor_repository = ProvedorRepositoryImpl()
        # Capa de Dominio
        provedor_service = ProvedorService(provedor_repository)
        # Capa de Aplicación
        provedor_use_case = ProvedorUseCase(provedor_service)
        # Capa de Presentación (Controladores)
        self.provedor_controller = ProvedorCmd(provedor_use_case)
        
        # Configuración del módulo de autorización
        self.authorization_service = create_authorization_module(
            self.app.config.get("JWT_SECRET"),
            self.app.config.get("ALGORITHM")
        )
    
    def _register_routes(self):
        """Registra todas las rutas de la aplicación."""
        # Activar middleware de autorización para seguridad del microservicio
        create_authorization_middleware(
            self.app,
            self.app.config.get("JWT_SECRET"),
            self.app.config.get("ALGORITHM")
        )
        
        # Registrar rutas de proveedores
        provedor_routes = create_provedor_routes(self.provedor_controller)
        self.app.register_blueprint(provedor_routes)
        
        # Registrar rutas de autorización (para que el Gateway pueda usar)
        from src.modules.autorizador.infraestructura.rutas.auth_routes import create_auth_routes
        from src.modules.autorizador.infraestructura.cmd.auth_cmd import AuthCmd
        from src.modules.autorizador.aplicacion.servicios.auth_service import AuthService
        
        # Crear servicio y controlador de autorización
        auth_service = AuthService(
            self.app.config.get("JWT_SECRET"),
            self.app.config.get("ALGORITHM")
        )
        auth_controller = AuthCmd(auth_service)
        auth_routes = create_auth_routes(auth_controller)
        self.app.register_blueprint(auth_routes)
        
        # Ruta raíz simple
        @self.app.route("/")
        def root():
            return {
                "message": "Microservicio de Provedores is running",
                "version": "2.0.0",
                "auth_middleware": True,
                "auth_service": True,
                "security": "Defense in depth - microservice validates tokens + internal request detection",
                "auth_endpoints": {
                    "validate": "/auth/validate",
                    "authorize": "/auth/authorize", 
                    "user_info": "/auth/user-info",
                    "resources": "/auth/resources"
                },
                "permissions": {
                    "ADMIN": "Full access to providers",
                    "MANAGER": "Full access to providers",
                    "USER": "NO ACCESS to providers",
                    "VIEWER": "NO ACCESS to providers"
                }
            }
        
        # Ruta de health check
        @self.app.route("/health")
        def health():
            return {
                "status": "healthy",
                "service": "provedores",
                "version": "2.0.0",
                "auth_enabled": True
            }
    
    def get_app(self) -> Flask:
        """
        Obtiene la aplicación Flask configurada.
        
        Returns:
            Flask: Aplicación Flask o None si no está creada
        """
        return self.app
