"""
Cliente de Apache Pulsar para comunicación asíncrona
"""
import json
import os
import logging
from typing import Dict, Any, Optional, Callable
import pulsar
from pulsar import Client, Producer, Consumer, Message

logger = logging.getLogger(__name__)


class PulsarClient:
    """Cliente de Pulsar para publicar y consumir eventos."""
    
    def __init__(self, service_url: str = None):
        """
        Inicializa el cliente de Pulsar.
        
        Args:
            service_url: URL del servicio Pulsar. Si no se proporciona, 
                        se obtiene de la variable de entorno PULSAR_SERVICE_URL
        """
        self.service_url = service_url or os.environ.get(
            'PULSAR_SERVICE_URL', 
            'pulsar://localhost:6650'
        )
        self.client: Optional[Client] = None
        self.producers: Dict[str, Producer] = {}
        self.consumers: Dict[str, Consumer] = {}
        
    def connect(self) -> None:
        """Establece conexión con Pulsar."""
        try:
            self.client = pulsar.Client(self.service_url)
            logger.info(f"Conectado a Pulsar en {self.service_url}")
        except Exception as e:
            logger.error(f"Error conectando a Pulsar: {e}")
            raise
    
    def disconnect(self) -> None:
        """Cierra la conexión con Pulsar."""
        try:
            # Cerrar todos los productores
            for producer in self.producers.values():
                producer.close()
            self.producers.clear()
            
            # Cerrar todos los consumidores
            for consumer in self.consumers.values():
                consumer.close()
            self.consumers.clear()
            
            # Cerrar cliente
            if self.client:
                self.client.close()
                self.client = None
                
            logger.info("Desconectado de Pulsar")
        except Exception as e:
            logger.error(f"Error desconectando de Pulsar: {e}")
    
    def get_producer(self, topic: str) -> Producer:
        """
        Obtiene o crea un productor para un tópico específico.
        
        Args:
            topic: Nombre del tópico
            
        Returns:
            Producer: Productor de Pulsar
        """
        if topic not in self.producers:
            if not self.client:
                self.connect()
                
            self.producers[topic] = self.client.create_producer(
                topic=topic,
                send_timeout_millis=30000,
                block_if_queue_full=True
            )
            logger.info(f"Productor creado para tópico: {topic}")
            
        return self.producers[topic]
    
    def publish_event(self, topic: str, event_data: Dict[str, Any], 
                     properties: Dict[str, str] = None) -> None:
        """
        Publica un evento en un tópico específico.
        
        Args:
            topic: Nombre del tópico
            event_data: Datos del evento
            properties: Propiedades adicionales del mensaje
        """
        try:
            producer = self.get_producer(topic)
            
            # Serializar datos del evento
            message_data = json.dumps(event_data).encode('utf-8')
            
            # Propiedades por defecto
            message_properties = properties or {}
            message_properties.update({
                'content-type': 'application/json',
                'source': 'gateway'
            })
            
            # Enviar mensaje
            producer.send(
                content=message_data,
                properties=message_properties
            )
            
            logger.info(f"Evento publicado en tópico {topic}: {event_data}")
            
        except Exception as e:
            logger.error(f"Error publicando evento en {topic}: {e}")
            raise
    
    def create_consumer(self, topic: str, subscription_name: str,
                       consumer_type: pulsar.ConsumerType = pulsar.ConsumerType.Shared,
                       message_handler: Callable[[Consumer, Message], None] = None) -> Consumer:
        """
        Crea un consumidor para un tópico específico.
        
        Args:
            topic: Nombre del tópico
            subscription_name: Nombre de la suscripción
            consumer_type: Tipo de consumidor
            message_handler: Función para manejar mensajes
            
        Returns:
            Consumer: Consumidor de Pulsar
        """
        if not self.client:
            self.connect()
            
        consumer_key = f"{topic}_{subscription_name}"
        
        if consumer_key not in self.consumers:
            self.consumers[consumer_key] = self.client.subscribe(
                topic=topic,
                subscription_name=subscription_name,
                consumer_type=consumer_type,
                message_listener=message_handler
            )
            logger.info(f"Consumidor creado para tópico {topic} con suscripción {subscription_name}")
            
        return self.consumers[consumer_key]
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


# Instancia global del cliente
pulsar_client = PulsarClient()
