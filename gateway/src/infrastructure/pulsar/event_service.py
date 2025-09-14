"""
Servicio de eventos para el gateway
"""
import json
import uuid
import time
import logging
from datetime import datetime
from typing import Dict, Any
import pulsar
from .pulsar_client import pulsar_client
from .event_types import EventType, TOPIC_MAPPING

logger = logging.getLogger(__name__)


class EventService:
    """Servicio para manejar eventos asincrónos en el gateway."""
    
    def __init__(self):
        """Inicializa el servicio de eventos."""
        self.response_consumers: Dict[str, pulsar.Consumer] = {}
        self._consumers_setup = False
    
    def _setup_response_consumers(self):
        """Configura consumidores para tópicos de respuesta."""
        try:
            # Consumidor para respuestas de productos
            self.response_consumers["productos"] = pulsar_client.client.subscribe(
                topic="productos-responses",
                subscription_name="gateway-productos-responses",
                consumer_type=pulsar.ConsumerType.Exclusive
            )
            
            # Consumidor para respuestas de proveedores
            self.response_consumers["provedores"] = pulsar_client.client.subscribe(
                topic="provedores-responses",
                subscription_name="gateway-provedores-responses", 
                consumer_type=pulsar.ConsumerType.Exclusive
            )
            
            logger.info("Consumidores de respuesta configurados")
            
        except Exception as e:
            logger.error(f"Error configurando consumidores de respuesta: {e}")
            raise
    
    def publish_event_and_wait_response(self, event_type: EventType, 
                                      event_data: Dict[str, Any],
                                      timeout: int = 30) -> Dict[str, Any]:
        """
        Publica un evento y espera la respuesta.
        
        Args:
            event_type: Tipo de evento
            event_data: Datos del evento
            timeout: Timeout en segundos
            
        Returns:
            Dict: Respuesta del microservicio
        """
        correlation_id = str(uuid.uuid4())
        
        try:
            # Configurar consumidores si no están configurados
            if not self._consumers_setup:
                self._setup_response_consumers()
                self._consumers_setup = True
            
            # Obtener tópico para el evento y respuesta
            topic = TOPIC_MAPPING.get(event_type)
            if not topic:
                raise ValueError(f"Tópico no encontrado para evento: {event_type}")
            
            # Determinar tópico de respuesta
            if "productos" in topic:
                response_consumer = self.response_consumers["productos"]
            elif "provedores" in topic:
                response_consumer = self.response_consumers["provedores"]
            else:
                raise ValueError(f"Consumidor de respuesta no encontrado para tópico: {topic}")
            
            # Agregar metadata al evento
            event_data.update({
                'correlation_id': correlation_id,
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'gateway'
            })
            
            # Publicar evento
            pulsar_client.publish_event(
                topic=topic,
                event_data=event_data,
                properties={
                    'correlation_id': correlation_id,
                    'event_type': event_type.value
                }
            )
            
            # Esperar respuesta usando polling
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    # Intentar recibir mensaje con timeout corto
                    message = response_consumer.receive(timeout_millis=1000)
                    
                    # Verificar correlation_id
                    msg_correlation_id = message.properties().get('correlation_id')
                    if msg_correlation_id == correlation_id:
                        # Mensaje correspondiente encontrado
                        response_data = json.loads(message.data().decode('utf-8'))
                        response_consumer.acknowledge(message)
                        return response_data
                    else:
                        # Mensaje de otra correlación, acknowledge para no bloquearlo
                        # pero no lo procesamos en este request
                        response_consumer.acknowledge(message)
                        logger.debug(f"Mensaje para correlación diferente: {msg_correlation_id}, esperando: {correlation_id}")
                        
                except pulsar.Timeout:
                    # Timeout normal, continuar esperando
                    continue
                except Exception as e:
                    logger.error(f"Error recibiendo mensaje: {e}")
                    continue
            
            # Timeout esperando respuesta
            raise TimeoutError(f"Timeout esperando respuesta para {correlation_id}")
            
        except Exception as e:
            logger.error(f"Error en publish_event_and_wait_response: {e}")
            raise
    
    def cleanup(self):
        """Limpia recursos del servicio."""
        try:
            for consumer in self.response_consumers.values():
                consumer.close()
            self.response_consumers.clear()
            logger.info("Servicio de eventos limpiado")
        except Exception as e:
            logger.error(f"Error limpiando servicio de eventos: {e}")
    
    def publish_producto_query_all(self, headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para obtener todos los productos."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PRODUCTO_QUERY_ALL,
            event_data={'headers': headers or {}}
        )
    
    def publish_producto_query_by_id(self, producto_id: str, 
                                   headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para obtener producto por ID."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PRODUCTO_QUERY_BY_ID,
            event_data={
                'producto_id': producto_id,
                'headers': headers or {}
            }
        )
    
    def publish_producto_query_by_category(self, categoria: str,
                                         headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para obtener productos por categoría."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PRODUCTO_QUERY_BY_CATEGORY,
            event_data={
                'categoria': categoria,
                'headers': headers or {}
            }
        )
    
    def publish_producto_search_by_name(self, nombre: str,
                                      headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para buscar productos por nombre."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PRODUCTO_SEARCH_BY_NAME,
            event_data={
                'nombre': nombre,
                'headers': headers or {}
            }
        )
    
    def publish_provedor_query_all(self, headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para obtener todos los proveedores."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PROVEDOR_QUERY_ALL,
            event_data={'headers': headers or {}}
        )
    
    def publish_provedor_query_by_id(self, provedor_id: int,
                                   headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para obtener proveedor por ID."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PROVEDOR_QUERY_BY_ID,
            event_data={
                'provedor_id': provedor_id,
                'headers': headers or {}
            }
        )
    
    def publish_provedor_query_by_nit(self, nit: int,
                                    headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para obtener proveedor por NIT."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PROVEDOR_QUERY_BY_NIT,
            event_data={
                'nit': nit,
                'headers': headers or {}
            }
        )
    
    def publish_provedor_query_by_country(self, pais: str,
                                        headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para obtener proveedores por país."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PROVEDOR_QUERY_BY_COUNTRY,
            event_data={
                'pais': pais,
                'headers': headers or {}
            }
        )
    
    def publish_provedor_search_by_name(self, nombre: str,
                                      headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Publica evento para buscar proveedores por nombre."""
        return self.publish_event_and_wait_response(
            event_type=EventType.PROVEDOR_SEARCH_BY_NAME,
            event_data={
                'nombre': nombre,
                'headers': headers or {}
            }
        )


# Instancia global del servicio de eventos
event_service = EventService()
