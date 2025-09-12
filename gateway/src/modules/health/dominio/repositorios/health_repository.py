from abc import ABC, abstractmethod

from ..entities import Health

class HealthRepository(ABC):
    @abstractmethod
    def get_health(self) -> Health: ...