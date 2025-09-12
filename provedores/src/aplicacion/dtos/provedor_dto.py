from dataclasses import dataclass
from enum import Enum


class PaisDto(Enum):
    COLOMBIA = "colombia"
    MEXICO = "mexico"
    ARGENTINA = "argentina"
    CHILE = "chile"
    PERU = "peru"
    BRASIL = "brasil"
    ECUADOR = "ecuador"
    VENEZUELA = "venezuela"
    URUGUAY = "uruguay"
    PARAGUAY = "paraguay"
    BOLIVIA = "bolivia"
    OTROS = "otros"


@dataclass(frozen=True)
class ProvedorDto:
    """
    DTO que representa un proveedor.
    """
    id: int
    nit: int
    nombre: str
    pais: PaisDto
    direccion: str
    telefono: int
    email: str
