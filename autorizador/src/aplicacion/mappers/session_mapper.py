from typing import Any, Dict
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.dominio.entities.session import Session

class SessionMapper:
    @staticmethod
    def entity_to_dto(session: Session) -> SessionDto:
        return SessionDto(
            id=session.id,
            user_id=session.user_id,
            token=session.token,
            expires_at=session.expires_at,
        )
    
    @staticmethod
    def dto_to_entity(session_dto: SessionDto) -> Session:
        return Session(
            id=session_dto.id,
            user_id=session_dto.user_id,
            token=session_dto.token,
            expires_at=session_dto.expires_at,
        )
    
    @staticmethod
    def dto_to_json(session_dto: SessionDto) -> Dict[str, Any]:
        return {
            "id": session_dto.id,
            "user_id": session_dto.user_id,
            "token": session_dto.token,
            "expires_at": session_dto.expires_at,
        }
    
    @staticmethod
    def json_to_dto(json: Dict[str, Any]) -> SessionDto:
        return SessionDto(
            id=json["id"],
            user_id=json["user_id"],
            token=json["token"],
            expires_at=json["expires_at"],
        )