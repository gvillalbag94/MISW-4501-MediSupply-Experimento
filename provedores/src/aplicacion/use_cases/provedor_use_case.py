from typing import List, Optional
from src.dominio.entities.provedor import Provedor
from src.aplicacion.servicios.provedor_service import ProvedorService


class ProvedorUseCase:
    """Caso de uso para la gestión de proveedores."""
    
    def __init__(self, provedor_service: ProvedorService):
        self.provedor_service = provedor_service
    
    def obtener_todos_los_provedores(self) -> List[Provedor]:
        """Obtiene todos los proveedores."""
        return self.provedor_service.obtener_todos_los_provedores()
    
    def obtener_provedor_por_id(self, provedor_id: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su ID."""
        return self.provedor_service.obtener_provedor_por_id(provedor_id)
    
    def obtener_provedor_por_nit(self, nit: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su NIT."""
        return self.provedor_service.obtener_provedor_por_nit(nit)
    
    def obtener_provedores_por_pais(self, pais: str) -> List[Provedor]:
        """Obtiene proveedores por país."""
        return self.provedor_service.obtener_provedores_por_pais(pais)
    
    def buscar_provedores_por_nombre(self, nombre: str) -> List[Provedor]:
        """Busca proveedores por nombre."""
        return self.provedor_service.buscar_provedores_por_nombre(nombre)
    
    def crear_provedor(self, provedor: Provedor) -> Provedor:
        """Crea un nuevo proveedor."""
        return self.provedor_service.crear_provedor(provedor)
    
    def actualizar_provedor(self, provedor: Provedor) -> Provedor:
        """Actualiza un proveedor existente."""
        return self.provedor_service.actualizar_provedor(provedor)
    
    def eliminar_provedor(self, provedor_id: int) -> bool:
        """Elimina un proveedor por su ID."""
        return self.provedor_service.eliminar_provedor(provedor_id)
