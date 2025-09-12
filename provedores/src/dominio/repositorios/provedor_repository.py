from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.entities.provedor import Provedor


class ProvedorRepository(ABC):
    """Interfaz del repositorio para proveedores."""
    
    @abstractmethod
    def obtener_todos(self) -> List[Provedor]:
        """Obtiene todos los proveedores."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, provedor_id: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su ID."""
        pass
    
    @abstractmethod
    def obtener_por_nit(self, nit: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su NIT."""
        pass
    
    @abstractmethod
    def obtener_por_pais(self, pais: str) -> List[Provedor]:
        """Obtiene proveedores por país."""
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Provedor]:
        """Busca proveedores por nombre."""
        pass
    
    @abstractmethod
    def crear(self, provedor: Provedor) -> Provedor:
        """Crea un nuevo proveedor."""
        pass
    
    @abstractmethod
    def actualizar(self, provedor: Provedor) -> Provedor:
        """Actualiza un proveedor existente."""
        pass
    
    @abstractmethod
    def eliminar(self, provedor_id: int) -> bool:
        """Elimina un proveedor por su ID."""
        pass
