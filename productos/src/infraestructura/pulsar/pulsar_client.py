"""
Cliente de Apache Pulsar para el microservicio de productos
"""
import json
import os
import logging
from typing import Dict, Any, Optional
import pulsar
from pulsar import Client, Producer, Consumer

logger = logging.getLogger(__name__)


class PulsarClient:
    """Cliente de Pulsar para el microservicio de productos."""
    
    def __init__(self, service_url: str = None):
        """
        Inicializa el cliente de Pulsar.
        
        Args:
            service_url: URL del servicio Pulsar
        """
        self.service_url = service_url or os.environ.get(
            'PULSAR_SERVICE_URL', 
            'pulsar://localhost:6650'
        )
        self.client: Optional[Client] = None
        self.producer: Optional[Producer] = None
        
    def connect(self) -> None:
        """Establece conexión con Pulsar."""
        try:
            self.client = pulsar.Client(self.service_url)
            # Crear productor para respuestas
            self.producer = self.client.create_producer(
                topic="productos-responses",
                send_timeout_millis=30000,
                block_if_queue_full=True
            )
            logger.info(f"Cliente de productos conectado a Pulsar en {self.service_url}")
        except Exception as e:
            logger.error(f"Error conectando a Pulsar: {e}")
            raise
    
    def disconnect(self) -> None:
        """Cierra la conexión con Pulsar."""
        try:
            if self.producer:
                self.producer.close()
                self.producer = None
                
            if self.client:
                self.client.close()
                self.client = None
                
            logger.info("Cliente de productos desconectado de Pulsar")
        except Exception as e:
            logger.error(f"Error desconectando de Pulsar: {e}")
    
    def send_response(self, response_data: Dict[str, Any], 
                     correlation_id: str) -> None:
        """
        Envía una respuesta al gateway.
        
        Args:
            response_data: Datos de respuesta
            correlation_id: ID de correlación
        """
        try:
            if not self.producer:
                self.connect()
                
            # Serializar datos de respuesta
            message_data = json.dumps(response_data).encode('utf-8')
            
            # Enviar mensaje con correlation_id
            self.producer.send(
                content=message_data,
                properties={
                    'correlation_id': correlation_id,
                    'content-type': 'application/json',
                    'source': 'productos'
                }
            )
            
            logger.info(f"Respuesta enviada para correlación {correlation_id}")
            
        except Exception as e:
            logger.error(f"Error enviando respuesta: {e}")
            raise
    
    def create_consumer(self, topic: str, subscription_name: str) -> Consumer:
        """
        Crea un consumidor para un tópico específico.
        
        Args:
            topic: Nombre del tópico
            subscription_name: Nombre de la suscripción
            
        Returns:
            Consumer: Consumidor de Pulsar
        """
        if not self.client:
            self.connect()
            
        consumer = self.client.subscribe(
            topic=topic,
            subscription_name=subscription_name,
            consumer_type=pulsar.ConsumerType.Shared
        )
        
        logger.info(f"Consumidor creado para tópico {topic}")
        return consumer
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


# Instancia global del cliente
pulsar_client = PulsarClient()
