"""
Consumidor de eventos para el microservicio de proveedores
"""
import json
import logging
import threading
from typing import Dict, Any
import pulsar
from flask import Flask
from .pulsar_client import pulsar_client
from src.infraestructura.cmd.provedor_cmd import ProvedorCmd

logger = logging.getLogger(__name__)


class EventConsumer:
    """Consumidor de eventos para el microservicio de proveedores."""
    
    def __init__(self, provedor_controller: ProvedorCmd, app: Flask = None):
        """
        Inicializa el consumidor de eventos.
        
        Args:
            provedor_controller: Controlador de proveedores
            app: Instancia de la aplicación Flask
        """
        self.provedor_controller = provedor_controller
        self.app = app
        self.consumer = None
        self.running = False
        self.consumer_thread = None
        
    def start_consuming(self):
        """Inicia el consumo de eventos."""
        try:
            pulsar_client.connect()
            
            # Crear consumidor para eventos de proveedores
            self.consumer = pulsar_client.create_consumer(
                topic="provedores-queries",
                subscription_name="provedores-service"
            )
            
            self.running = True
            
            # Iniciar hilo de consumo
            self.consumer_thread = threading.Thread(
                target=self._consume_messages,
                daemon=True
            )
            self.consumer_thread.start()
            
            logger.info("Consumidor de eventos de proveedores iniciado")
            
        except Exception as e:
            logger.error(f"Error iniciando consumidor: {e}")
            raise
    
    def stop_consuming(self):
        """Detiene el consumo de eventos."""
        try:
            self.running = False
            
            if self.consumer_thread:
                self.consumer_thread.join(timeout=5)
                
            if self.consumer:
                self.consumer.close()
                self.consumer = None
                
            pulsar_client.disconnect()
            
            logger.info("Consumidor de eventos de proveedores detenido")
            
        except Exception as e:
            logger.error(f"Error deteniendo consumidor: {e}")
    
    def _consume_messages(self):
        """Bucle principal de consumo de mensajes."""
        while self.running:
            try:
                # Recibir mensaje con timeout
                message = self.consumer.receive(timeout_millis=1000)
                
                # Procesar mensaje
                self._process_message(message)
                
                # Confirmar mensaje
                self.consumer.acknowledge(message)
                
            except pulsar.Timeout:
                # Timeout normal, continuar
                continue
            except Exception as e:
                logger.error(f"Error procesando mensaje: {e}")
                if 'message' in locals():
                    self.consumer.negative_acknowledge(message)
    
    def _process_message(self, message: pulsar.Message):
        """
        Procesa un mensaje recibido.
        
        Args:
            message: Mensaje de Pulsar
        """
        try:
            # Obtener datos del mensaje
            event_data = json.loads(message.data().decode('utf-8'))
            correlation_id = message.properties().get('correlation_id')
            event_type = message.properties().get('event_type')
            
            logger.info(f"Procesando evento {event_type} con correlación {correlation_id}")
            
            # Procesar según tipo de evento
            response = self._handle_event(event_type, event_data)
            
            # Enviar respuesta
            if correlation_id:
                pulsar_client.send_response(response, correlation_id)
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            raise
    
    def _execute_with_context(self, controller_method, *args, **kwargs):
        """Ejecuta un método del controlador con el contexto Flask apropiado."""
        if self.app:
            with self.app.app_context():
                return controller_method(*args, **kwargs)
        else:
            return controller_method(*args, **kwargs)
    
    def _format_response(self, result, default_status=200):
        """Formatea la respuesta del controlador para ser serializable."""
        # Si el resultado es una tupla (response, status_code)
        if isinstance(result, tuple):
            response_data, status_code = result
            # Si response_data es un objeto Response, obtener los datos JSON
            if hasattr(response_data, 'get_json'):
                response_dict = response_data.get_json()
                response_dict["status_code"] = status_code
                return response_dict
            else:
                response_data["status_code"] = status_code
                return response_data
        else:
            # Si result es un objeto Response, obtener los datos JSON
            if hasattr(result, 'get_json'):
                response_dict = result.get_json()
                response_dict["status_code"] = default_status
                return response_dict
            else:
                result["status_code"] = default_status
                return result
    
    def _handle_event(self, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maneja un evento específico.
        
        Args:
            event_type: Tipo de evento
            event_data: Datos del evento
            
        Returns:
            Dict: Respuesta del evento
        """
        try:
            if event_type == "provedor.query.all":
                return self._handle_query_all(event_data)
            elif event_type == "provedor.query.by_id":
                return self._handle_query_by_id(event_data)
            elif event_type == "provedor.query.by_nit":
                return self._handle_query_by_nit(event_data)
            elif event_type == "provedor.query.by_country":
                return self._handle_query_by_country(event_data)
            elif event_type == "provedor.search.by_name":
                return self._handle_search_by_name(event_data)
            else:
                logger.warning(f"Tipo de evento no soportado: {event_type}")
                return {
                    "success": False,
                    "error": f"Tipo de evento no soportado: {event_type}",
                    "status_code": 400
                }
                
        except Exception as e:
            logger.error(f"Error manejando evento {event_type}: {e}")
            return {
                "success": False,
                "error": f"Error interno del servidor: {str(e)}",
                "status_code": 500
            }
    
    def _handle_query_all(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja consulta de todos los proveedores."""
        try:
            result = self._execute_with_context(
                self.provedor_controller.obtener_todos_los_provedores
            )
            return self._format_response(result)
                
        except Exception as e:
            logger.error(f"Error obteniendo todos los proveedores: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def _handle_query_by_id(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja consulta de proveedor por ID."""
        try:
            provedor_id = event_data.get('provedor_id')
            if provedor_id is None:
                return {
                    "success": False,
                    "error": "provedor_id es requerido",
                    "status_code": 400
                }
            
            result = self._execute_with_context(
                self.provedor_controller.obtener_provedor_por_id, provedor_id
            )
            return self._format_response(result)
            
            # Si el resultado es una tupla (response, status_code)
            if isinstance(result, tuple):
                response_data, status_code = result
                response_data["status_code"] = status_code
                return response_data
            else:
                result["status_code"] = 200
                return result
                
        except Exception as e:
            logger.error(f"Error obteniendo proveedor por ID: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def _handle_query_by_nit(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja consulta de proveedor por NIT."""
        try:
            nit = event_data.get('nit')
            if nit is None:
                return {
                    "success": False,
                    "error": "nit es requerido",
                    "status_code": 400
                }
            
            result = self._execute_with_context(
                self.provedor_controller.obtener_provedor_por_nit, nit
            )
            return self._format_response(result)
            
            # Si el resultado es una tupla (response, status_code)
            if isinstance(result, tuple):
                response_data, status_code = result
                response_data["status_code"] = status_code
                return response_data
            else:
                result["status_code"] = 200
                return result
                
        except Exception as e:
            logger.error(f"Error obteniendo proveedor por NIT: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def _handle_query_by_country(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja consulta de proveedores por país."""
        try:
            pais = event_data.get('pais')
            if not pais:
                return {
                    "success": False,
                    "error": "pais es requerido",
                    "status_code": 400
                }
            
            result = self._execute_with_context(
                self.provedor_controller.obtener_provedores_por_pais, pais
            )
            return self._format_response(result)
            
            # Si el resultado es una tupla (response, status_code)
            if isinstance(result, tuple):
                response_data, status_code = result
                response_data["status_code"] = status_code
                return response_data
            else:
                result["status_code"] = 200
                return result
                
        except Exception as e:
            logger.error(f"Error obteniendo proveedores por país: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def _handle_search_by_name(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja búsqueda de proveedores por nombre."""
        try:
            nombre = event_data.get('nombre')
            if not nombre:
                return {
                    "success": False,
                    "error": "nombre es requerido",
                    "status_code": 400
                }
            
            result = self._execute_with_context(
                self.provedor_controller.buscar_provedores_por_nombre, nombre
            )
            return self._format_response(result)
            
            # Si el resultado es una tupla (response, status_code)
            if isinstance(result, tuple):
                response_data, status_code = result
                response_data["status_code"] = status_code
                return response_data
            else:
                result["status_code"] = 200
                return result
                
        except Exception as e:
            logger.error(f"Error buscando proveedores por nombre: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }


# Instancia global del consumidor (se inicializará en main.py)
event_consumer = None
