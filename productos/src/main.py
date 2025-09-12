import logging
from src.infraestructura.config import Config

def setup_logging(app):
    """Configura el sistema de logging."""
    log_level = app.config.get("LOG_LEVEL", "INFO").upper()
    
    # Configurar el logger principal
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Configurar el logger específico para requests
    request_logger = logging.getLogger("request_logger")
    request_logger.setLevel(getattr(logging, log_level))
    
    # Evitar que se dupliquen los logs
    if not request_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        request_logger.addHandler(handler)
        request_logger.propagate = False


def create_application():
    """
    Factory function para crear la aplicación.
    
    Returns:
        Flask: Aplicación Flask configurada
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Crear configuración de Flask
        flask_config = Config()
        
        # Crear aplicación
        app = flask_config.create_app()
        setup_logging(app)
        
        # Inicializar la aplicación
        logger.info("Microservicio de Productos initialized successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to initialize Microservicio de Productos: {str(e)}")
        raise


# Crear instancia de la aplicación
app = create_application()


if __name__ == "__main__":
    # Configuración para desarrollo
    host = app.config.get("HOST", "0.0.0.0")
    port = app.config.get("PORT", 5001)
    debug = app.config.get("DEBUG", False)
    
    print(f"Starting Microservicio de Productos on {host}:{port}")
    print(f"Health check available at: http://{host}:{port}/health")
    print(f"Debug mode: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
