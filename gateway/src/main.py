import logging
from config import Config
from flask import Flask

def setup_logging(app: Flask):
    """Configura el sistema de logging."""
    log_level = app.config.get('LOG_LEVEL', 'INFO').upper()
    
    # Configurar el logger principal
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
    )
    
    # Configurar el logger específico para requests
    request_logger = logging.getLogger('request_logger')
    request_logger.setLevel(getattr(logging, log_level))
    
    # Evitar que se dupliquen los logs
    if not request_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        request_logger.addHandler(handler)
        request_logger.propagate = False


def create_application():
    """
    Factory function para crear la aplicación.
    
    Returns:
        Flask: Aplicación Flask configurada
    """
   
    
    try:
        # Crear configuración de Flask
        flask_config = Config()

        # Crear aplicación
        app = flask_config.create_app()
        setup_logging(app)
        logger = logging.getLogger(__name__)
        
        # Inicializar la aplicación
        logger.info("API Gateway initialized successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to initialize API Gateway: {str(e)}")
        raise


# Crear instancia de la aplicación
app = create_application()


if __name__ == '__main__':
    # Configuración para desarrollo
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    print(f"Starting API Gateway on {host}:{port}")
    print(f"Health check available at: http://{host}:{port}/health/")
    print(f"Debug mode: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )