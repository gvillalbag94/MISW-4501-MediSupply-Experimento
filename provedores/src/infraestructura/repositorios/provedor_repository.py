from typing import List, Optional
from src.dominio.entities.provedor import Provedor, Pais
from src.dominio.repositorios.provedor_repository import ProvedorRepository


class ProvedorRepositoryImpl(ProvedorRepository):
    """Implementación del repositorio de proveedores con datos en memoria."""
    
    def __init__(self):
        # Datos de ejemplo en memoria
        self._provedores = [
            Provedor(
                id=1,
                nit=900123456,
                nombre="Tecnología Avanzada S.A.S",
                pais=Pais.COLOMBIA,
                direccion="Calle 123 #45-67, Bogotá",
                telefono=6012345678,
                email="contacto@tecnologiaavanzada.com"
            ),
            Provedor(
                id=2,
                nit=800987654,
                nombre="Distribuidora Nacional Ltda",
                pais=Pais.COLOMBIA,
                direccion="Carrera 80 #12-34, Medellín",
                telefono=6045678901,
                email="ventas@distribuidoranacional.com"
            ),
            Provedor(
                id=3,
                nit=123456789,
                nombre="Importaciones del Sur S.A",
                pais=Pais.CHILE,
                direccion="Av. Providencia 1234, Santiago",
                telefono=56212345678,
                email="info@importacionessur.cl"
            ),
            Provedor(
                id=4,
                nit=987654321,
                nombre="Comercializadora Andina",
                pais=Pais.ECUADOR,
                direccion="Av. Amazonas 987, Quito",
                telefono=593212345678,
                email="comercial@andina.ec"
            ),
            Provedor(
                id=5,
                nit=456789123,
                nombre="Proveedores Unidos S.A.C",
                pais=Pais.PERU,
                direccion="Jr. Lima 456, Lima",
                telefono=51123456789,
                email="unidos@proveedores.pe"
            ),
            Provedor(
                id=6,
                nit=789123456,
                nombre="Distribuidora del Norte",
                pais=Pais.MEXICO,
                direccion="Av. Insurgentes 789, Ciudad de México",
                telefono=525512345678,
                email="norte@distribuidora.mx"
            )
        ]
    
    def obtener_todos(self) -> List[Provedor]:
        """Obtiene todos los proveedores."""
        return self._provedores.copy()
    
    def obtener_por_id(self, provedor_id: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su ID."""
        for provedor in self._provedores:
            if provedor.id == provedor_id:
                return provedor
        return None
    
    def obtener_por_nit(self, nit: int) -> Optional[Provedor]:
        """Obtiene un proveedor por su NIT."""
        for provedor in self._provedores:
            if provedor.nit == nit:
                return provedor
        return None
    
    def obtener_por_pais(self, pais: str) -> List[Provedor]:
        """Obtiene proveedores por país."""
        return [p for p in self._provedores if p.pais.value == pais.lower()]
    
    def buscar_por_nombre(self, nombre: str) -> List[Provedor]:
        """Busca proveedores por nombre."""
        nombre_lower = nombre.lower()
        return [p for p in self._provedores if nombre_lower in p.nombre.lower()]
    
    def crear(self, provedor: Provedor) -> Provedor:
        """Crea un nuevo proveedor."""
        # Generar nuevo ID
        max_id = max([p.id for p in self._provedores]) if self._provedores else 0
        new_provedor = Provedor(
            id=max_id + 1,
            nit=provedor.nit,
            nombre=provedor.nombre,
            pais=provedor.pais,
            direccion=provedor.direccion,
            telefono=provedor.telefono,
            email=provedor.email
        )
        self._provedores.append(new_provedor)
        return new_provedor
    
    def actualizar(self, provedor: Provedor) -> Provedor:
        """Actualiza un proveedor existente."""
        for i, p in enumerate(self._provedores):
            if p.id == provedor.id:
                self._provedores[i] = provedor
                return provedor
        raise ValueError(f"Proveedor con ID {provedor.id} no encontrado")
    
    def eliminar(self, provedor_id: int) -> bool:
        """Elimina un proveedor por su ID."""
        for i, p in enumerate(self._provedores):
            if p.id == provedor_id:
                del self._provedores[i]
                return True
        return False
