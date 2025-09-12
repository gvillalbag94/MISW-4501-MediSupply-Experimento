from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class HealthDto:
    """
    DTO que representa el estado de salud.
    """
    status: str
    timestamp: datetime
    version: str