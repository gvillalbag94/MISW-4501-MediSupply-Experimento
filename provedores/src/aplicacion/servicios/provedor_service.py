from typing import List, Optional
from src.dominio.entities.provedor import Provedor
from src.dominio.repositorios.provedor_repository import ProvedorRepository


class ProvedorService:
    """Servicio de dominio para proveedores."""
    
    def __init__(self, provedor_repository: ProvedorRepository):
        self.provedor_repository = provedor_repository
    
    def obtener_todos_los_provedores(self) -> List[Provedor]:
        """Obtiene todos los proveedores."""
        return self.provedor_repository.obtener_todos()
    
    def obtener_provedor_por_id(self, provedor_id: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su ID."""
        return self.provedor_repository.obtener_por_id(provedor_id)
    
    def obtener_provedor_por_nit(self, nit: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su NIT."""
        return self.provedor_repository.obtener_por_nit(nit)
    
    def obtener_provedores_por_pais(self, pais: str) -> List[Provedor]:
        """Obtiene proveedores por país."""
        return self.provedor_repository.obtener_por_pais(pais)
    
    def buscar_provedores_por_nombre(self, nombre: str) -> List[Provedor]:
        """Busca proveedores por nombre."""
        return self.provedor_repository.buscar_por_nombre(nombre)
    
    def crear_provedor(self, provedor: Provedor) -> Provedor:
        """Crea un nuevo proveedor."""
        return self.provedor_repository.crear(provedor)
    
    def actualizar_provedor(self, provedor: Provedor) -> Provedor:
        """Actualiza un proveedor existente."""
        return self.provedor_repository.actualizar(provedor)
    
    def eliminar_provedor(self, provedor_id: int) -> bool:
        """Elimina un proveedor por su ID."""
        return self.provedor_repository.eliminar(provedor_id)
