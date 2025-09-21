import os
from dotenv import load_dotenv
from flask import Flask, g, request
from datetime import datetime
import logging

from src.infraestructura.cmd.producto_cmd import ProductoCmd
from src.aplicacion.servicios.producto_service import ProductoService
from src.infraestructura.repositorios.producto_repository import ProductoRepositoryImpl
from src.aplicacion.use_cases.producto_use_case import ProductoUseCase
from src.infraestructura.rutas.producto_routes import create_producto_routes
from src.infraestructura.pulsar.event_consumer import EventConsumer

load_dotenv(".env")


class Config:
    """
    Configuración y factory para la aplicación Flask.
    Maneja la inyección de dependencias siguiendo los principios de arquitectura hexagonal.
    """
    
    def __init__(self):
        self.app = None
        self.event_consumer = None
    
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
        
        # Configurar consumidor de eventos
        self._setup_event_consumer()
        
        # Registrar rutas
        self._register_routes()
        
        return self.app
    
    def _configure_app(self):
        """Configura parámetros básicos de la aplicación."""
        self.app.config["ENV"] = os.getenv("ENV", "development")
        self.app.config["DEBUG"] = os.getenv("DEBUG", "False").lower() == "true"
        self.app.config["HOST"] = os.getenv("HOST", "0.0.0.0")
        self.app.config["PORT"] = int(os.getenv("PORT", 6001))
        self.app.config["LOG_LEVEL"] = os.getenv("LOG_LEVEL", "INFO")
    
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
        producto_repository = ProductoRepositoryImpl()
        # Capa de Dominio
        producto_service = ProductoService(producto_repository)
        # Capa de Aplicación
        producto_use_case = ProductoUseCase(producto_service)
        # Capa de Presentación (Controladores)
        self.producto_controller = ProductoCmd(producto_use_case)
    
    def _setup_event_consumer(self):
        """Configura el consumidor de eventos de Pulsar."""
        try:
            self.event_consumer = EventConsumer(self.producto_controller, self.app)
            self.event_consumer.start_consuming()
            
            # Configurar limpieza al cerrar la aplicación
            import atexit
            atexit.register(self._cleanup_on_exit)
                    
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error configurando consumidor de eventos: {e}")
            # No lanzar excepción para permitir que el servicio funcione sin eventos
    
    def _register_routes(self):
        """Registra todas las rutas de la aplicación."""
        # Registrar rutas de productos
        producto_routes = create_producto_routes(self.producto_controller)
        self.app.register_blueprint(producto_routes)
        
        # Ruta raíz simple
        @self.app.route("/")
        def root():
            return {
                "message": "Microservicio de Productos is running",
                "version": "1.0.0",
            }
        
        # Ruta de health check
        @self.app.route("/health")
        def health():
            return {
                "status": "healthy",
                "service": "productos",
                "version": "1.0.0"
            }
    
    def _cleanup_on_exit(self):
        """Limpia recursos al cerrar la aplicación."""
        if self.event_consumer:
            try:
                self.event_consumer.stop_consuming()
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Error limpiando consumidor: {e}")
    
    def get_app(self) -> Flask:
        """
        Obtiene la aplicación Flask configurada.
        
        Returns:
            Flask: Aplicación Flask o None si no está creada
        """
        return self.app
