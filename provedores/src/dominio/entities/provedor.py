from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class Pais(Enum):
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
class Provedor:
    """
    Entidad del dominio que representa un proveedor.
    """
    id: int
    nit: int
    nombre: str
    pais: Pais
    direccion: str
    telefono: int
    email: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario."""
        return {
            "id": self.id,
            "nit": self.nit,
            "nombre": self.nombre,
            "pais": self.pais.value,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "email": self.email,
        }
