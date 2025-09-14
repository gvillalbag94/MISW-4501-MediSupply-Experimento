"""
Infraestructura de Apache Pulsar para el microservicio de productos
"""
from .pulsar_client import PulsarClient, pulsar_client
from .event_consumer import EventConsumer, event_consumer

__all__ = ['PulsarClient', 'pulsar_client', 'EventConsumer', 'event_consumer']
