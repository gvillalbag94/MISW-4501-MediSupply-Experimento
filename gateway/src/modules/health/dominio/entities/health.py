from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class Health:
    """
    Entidad del dominio que representa el estado de salud.
    """
    status: str
    timestamp: datetime
    version: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
        }
    
    @classmethod
    def healthy(cls, version: str = "1.0.0") -> 'Health':
        """Factory method para crear un estado saludable."""
        return cls(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version=version,
        )
    
    @classmethod
    def unhealthy(cls, version: str = "1.0.0") -> 'Health':
        """Factory method para crear un estado no saludable."""
        return cls(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            version=version,
        )