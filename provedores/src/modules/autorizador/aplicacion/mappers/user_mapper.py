from typing import Dict, Any
from modules.autenticador.dominio.entities.user import User, Role
from modules.autenticador.aplicacion.dtos.user_dto import UserDto, RoleDto

class UserMapper:
    @staticmethod
    def json_to_dto(user: Dict[str, Any]) -> UserDto:
        return UserDto(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            password=user["password"],
            role=RoleDto(user["role"]),
            token=user["token"],
        )   
    
    @staticmethod
    def dto_to_json(user_dto: UserDto) -> Dict[str, Any]:
        return {
            "id": user_dto.id,
            "name": user_dto.name,
            "email": user_dto.email,
            "password": user_dto.password,
            "role": user_dto.role.value,
            "token": user_dto.token,
        }
    
    @staticmethod
    def dto_to_entity(user_dto: UserDto) -> User:
        role = Role(user_dto.role.value)
        return User(
            id=user_dto.id,
            name=user_dto.name,
            email=user_dto.email,
            password=user_dto.password,
            role=role,
            token=user_dto.token,
        )
    
    @staticmethod
    def entity_to_dto(user: User) -> UserDto:
        role = RoleDto(user.role.value)
        return UserDto(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            role=role,
            token=user.token,
        )
    