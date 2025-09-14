"""
Definición de tipos de eventos para comunicación asíncrona
"""
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class EventType(Enum):
    """Tipos de eventos del sistema."""
    
    # Eventos de productos
    PRODUCTO_QUERY_ALL = "producto.query.all"
    PRODUCTO_QUERY_BY_ID = "producto.query.by_id"
    PRODUCTO_QUERY_BY_CATEGORY = "producto.query.by_category"
    PRODUCTO_SEARCH_BY_NAME = "producto.search.by_name"
    
    # Eventos de proveedores
    PROVEDOR_QUERY_ALL = "provedor.query.all"
    PROVEDOR_QUERY_BY_ID = "provedor.query.by_id"
    PROVEDOR_QUERY_BY_NIT = "provedor.query.by_nit"
    PROVEDOR_QUERY_BY_COUNTRY = "provedor.query.by_country"
    PROVEDOR_SEARCH_BY_NAME = "provedor.search.by_name"


@dataclass
class BaseEvent:
    """Evento base para todos los eventos del sistema."""
    
    event_type: EventType
    correlation_id: str
    timestamp: str
    source: str
    user_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el evento a diccionario."""
        return {
            'event_type': self.event_type.value,
            'correlation_id': self.correlation_id,
            'timestamp': self.timestamp,
            'source': self.source,
            'user_id': self.user_id
        }


@dataclass
class ProductoEvent(BaseEvent):
    """Evento relacionado con productos."""
    
    producto_id: Optional[str] = None
    categoria: Optional[str] = None
    nombre: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el evento a diccionario."""
        data = super().to_dict()
        data.update({
            'producto_id': self.producto_id,
            'categoria': self.categoria,
            'nombre': self.nombre,
            'filters': self.filters
        })
        return data


@dataclass
class ProvedorEvent(BaseEvent):
    """Evento relacionado con proveedores."""
    
    provedor_id: Optional[int] = None
    nit: Optional[int] = None
    pais: Optional[str] = None
    nombre: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el evento a diccionario."""
        data = super().to_dict()
        data.update({
            'provedor_id': self.provedor_id,
            'nit': self.nit,
            'pais': self.pais,
            'nombre': self.nombre,
            'filters': self.filters
        })
        return data


# Mapeo de tópicos por tipo de evento
TOPIC_MAPPING = {
    # Productos
    EventType.PRODUCTO_QUERY_ALL: "productos-queries",
    EventType.PRODUCTO_QUERY_BY_ID: "productos-queries",
    EventType.PRODUCTO_QUERY_BY_CATEGORY: "productos-queries",
    EventType.PRODUCTO_SEARCH_BY_NAME: "productos-queries",
    
    # Proveedores
    EventType.PROVEDOR_QUERY_ALL: "provedores-queries",
    EventType.PROVEDOR_QUERY_BY_ID: "provedores-queries",
    EventType.PROVEDOR_QUERY_BY_NIT: "provedores-queries",
    EventType.PROVEDOR_QUERY_BY_COUNTRY: "provedores-queries",
    EventType.PROVEDOR_SEARCH_BY_NAME: "provedores-queries",
}

# Tópicos de respuesta
RESPONSE_TOPICS = {
    "productos-queries": "productos-responses",
    "provedores-queries": "provedores-responses",
}
