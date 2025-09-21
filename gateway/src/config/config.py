from datetime import datetime, time
import logging
from dotenv import load_dotenv

import os
from flask import Flask, g, request

from modules.provedores.infraestructura.rutas.provedores_routes import create_provedores_routes
from modules.health.infraestructura.cmd import HealthCmd
from modules.health.aplicacion.servicios import HealthService
from modules.health.infraestructura.repositorios import HealthRepositoryImpl
from modules.health.infraestructura.rutas.health_routes import create_health_routes
from modules.health.aplicacion.use_cases.health_use_case import HealthUseCase
from modules.autenticador.aplicacion.servicios.auth_service import AuthService
from modules.autenticador.aplicacion.use_cases.auth_use_case import AuthUseCase
from modules.autenticador.infraestructura.cmd.auth_cmd import AuthCmd
from modules.autenticador.infraestructura.repositorios.auth_repository import AuthRepositoryImpl
from modules.autenticador.infraestructura.rutas.auth_routes import create_auth_routes
from modules.productos.infraestructura.rutas.producto_routes import create_producto_routes


load_dotenv('.env')

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
        
        # Configurar servicios externos para health check
        self._configure_external_services()
        
        # Inyección de dependencias
        self._setup_dependencies()
        
        # Registrar rutas
        self._register_routes()
        
        return self.app
    
    def _configure_app(self):
        """Configura parámetros básicos de la aplicación."""
        self.app.config['ENV'] = os.getenv('ENV', 'development')
        self.app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
        self.app.config['HOST'] = os.getenv('HOST', '0.0.0.0')
        self.app.config['PORT'] = int(os.getenv('PORT', 5000))
        self.app.config['LOG_LEVEL'] = os.getenv('LOG_LEVEL', 'INFO')
        self.app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', 'your-secret-key-here-with-32-plus-chars-for-security')
        self.app.config['ALGORITHM'] = os.getenv('ALGORITHM', 'HS256')
        self.app.config['PRODUCTOS_SERVICE_URL'] = os.getenv('PRODUCTOS_SERVICE_URL', 'http://127.0.0.1:5001')
        self.app.config['PROVEDORES_SERVICE_URL'] = os.getenv('PROVEDORES_SERVICE_URL', 'http://127.0.0.1:5003')

    def _configure_request_logging(self):
        """Configura el middleware para logging de requests y responses."""
        logger = logging.getLogger('request_logger')
        
        @self.app.before_request
        def log_request():
            """Log cuando entra una petición."""
            g.start_time = datetime.now().time()
            logger.info(f"INCOMING REQUEST: {request.method} {request.url}")
            
            # Log headers si está en modo debug
            if self.app.config.get('DEBUG'):
                logger.debug(f"Headers: {dict(request.headers)}")
                if request.is_json:
                    logger.debug(f"Request Body: {request.get_json()}")
        
        @self.app.after_request
        def log_response(response):
            """Log cuando sale una respuesta."""
            if hasattr(g, 'start_time'):
                duration = (datetime.now() - datetime.combine(datetime.today(), g.start_time)).total_seconds()
                logger.info(f"OUTGOING RESPONSE: {response.status_code} - Duration: {duration * 1000:.0f}ms - Size: {len(response.get_data())} bytes")
            else:
                logger.info(f"OUTGOING RESPONSE: {response.status_code}")
            return response

    
    def _configure_external_services(self):
        # """Configura los servicios externos para monitoreo."""
        # # Ejemplo de configuración de servicios externos
        # # Estos pueden venir de variables de entorno o configuración
        # self._external_services = {
        #     # "database": "http://database:5432/health",
        #     # "redis": "http://redis:6379/ping",
        #     # "external_api": "https://api.external.com/health"
        # }
        
        # # Cargar desde variables de entorno si existen
        # external_services_env = os.getenv('EXTERNAL_SERVICES')
        # if external_services_env:
        #     # Formato esperado: "service1:url1,service2:url2"
        #     for service_config in external_services_env.split(','):
        #         if ':' in service_config:
        #             name, url = service_config.split(':', 1)
        #             self._external_services[name.strip()] = url.strip()
        ...
    
    def _setup_dependencies(self):
        """Configura la inyección de dependencias siguiendo arquitectura hexagonal."""
        # Capa de Infraestructura
        health_repository = HealthRepositoryImpl()
        # Capa de Dominio
        health_service = HealthService(health_repository)
        # Capa de Aplicación
        health_check_use_case = HealthUseCase(health_service)
        # Capa de Presentación (Controladores)
        self.health_controller = HealthCmd(health_check_use_case)

        auth_repository = AuthRepositoryImpl(self.app.config.get('JWT_SECRET'), self.app.config.get('ALGORITHM'))
        auth_service = AuthService(auth_repository, self.app.config.get('JWT_SECRET'), self.app.config.get('ALGORITHM'))
        auth_use_case = AuthUseCase(auth_service)
        self.auth_controller = AuthCmd(auth_use_case)
    
    def _register_routes(self):
        """Registra todas las rutas de la aplicación."""
        # Registrar rutas de health
        health_routes = create_health_routes(self.health_controller)
        self.app.register_blueprint(health_routes)

        auth_routes = create_auth_routes(self.auth_controller)
        self.app.register_blueprint(auth_routes)

        productos_routes = create_producto_routes()
        self.app.register_blueprint(productos_routes)

        provedores_routes = create_provedores_routes()
        self.app.register_blueprint(provedores_routes)

        # Ruta raíz simple
        @self.app.route('/')
        def root():
            return {
                "message": "API Gateway is running",
                "version": "1.0.0",
            }
    
    def get_app(self) -> Flask:
        """
        Obtiene la aplicación Flask configurada.
        
        Returns:
            Flask: Aplicación Flask o None si no está creada
        """
        return self.app