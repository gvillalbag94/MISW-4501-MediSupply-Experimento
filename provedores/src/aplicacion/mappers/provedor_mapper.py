from src.dominio.entities.provedor import Provedor, Pais
from src.aplicacion.dtos.provedor_dto import ProvedorDto, PaisDto


class ProvedorMapper:
    """Mapper para convertir entre entidades y DTOs de proveedores."""
    
    @staticmethod
    def entity_to_dto(provedor: Provedor) -> ProvedorDto:
        """Convierte una entidad Provedor a ProvedorDto."""
        return ProvedorDto(
            id=provedor.id,
            nit=provedor.nit,
            nombre=provedor.nombre,
            pais=PaisDto(provedor.pais.value),
            direccion=provedor.direccion,
            telefono=provedor.telefono,
            email=provedor.email
        )
    
    @staticmethod
    def dto_to_entity(provedor_dto: ProvedorDto) -> Provedor:
        """Convierte un ProvedorDto a entidad Provedor."""
        return Provedor(
            id=provedor_dto.id,
            nit=provedor_dto.nit,
            nombre=provedor_dto.nombre,
            pais=Pais(provedor_dto.pais.value),
            direccion=provedor_dto.direccion,
            telefono=provedor_dto.telefono,
            email=provedor_dto.email
        )
    
    @staticmethod
    def entities_to_dtos(provedores: list[Provedor]) -> list[ProvedorDto]:
        """Convierte una lista de entidades Provedor a lista de ProvedorDto."""
        return [ProvedorMapper.entity_to_dto(provedor) for provedor in provedores]
    
    @staticmethod
    def dto_to_dict(provedor_dto: ProvedorDto) -> dict:
        """Convierte un ProvedorDto a diccionario para serialización JSON."""
        return {
            "id": provedor_dto.id,
            "nit": provedor_dto.nit,
            "nombre": provedor_dto.nombre,
            "pais": provedor_dto.pais.value,
            "direccion": provedor_dto.direccion,
            "telefono": provedor_dto.telefono,
            "email": provedor_dto.email
        }
    
    @staticmethod
    def dtos_to_dicts(provedores_dto: list[ProvedorDto]) -> list[dict]:
        """Convierte una lista de ProvedorDto a lista de diccionarios para serialización JSON."""
        return [ProvedorMapper.dto_to_dict(provedor_dto) for provedor_dto in provedores_dto]
