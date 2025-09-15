import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from ...dominio.entities import User, Token, Session, Role, TokenType, TokenStatus
from ...dominio.repositorios import AuthRepository, TokenRepository, SessionRepository


# Base de datos en memoria para pruebas
USERS_DB: Dict[str, Dict[str, Any]] = {
    "1": {
        "id": "1",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "User1234*",
        "role": "user",
        "is_active": True
    },
    "2": {
        "id": "2",
        "name": "Admin Doe",
        "email": "admin.doe@example.com",
        "password": "Admin1234*",
        "role": "admin",
        "is_active": True
    },
    "3": {
        "id": "3",
        "name": "Manager Doe",
        "email": "manager.doe@example.com",
        "password": "Manager1234*",
        "role": "manager",
        "is_active": True
    }
}

TOKENS_DB: Dict[str, Dict[str, Any]] = {}
SESSIONS_DB: Dict[str, Dict[str, Any]] = {}


class AuthRepositoryImpl(AuthRepository):
    """Implementación en memoria del repositorio de autenticación."""
    
    def find_user_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por email."""
        for user_data in USERS_DB.values():
            if user_data["email"] == email:
                return self._dict_to_user(user_data)
        return None
    
    def find_user_by_id(self, user_id: str) -> Optional[User]:
        """Busca un usuario por ID."""
        user_data = USERS_DB.get(user_id)
        if user_data:
            return self._dict_to_user(user_data)
        return None
    
    def save_user(self, user: User) -> User:
        """Guarda un usuario."""
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "role": user.role.value,
            "is_active": user.is_active
        }
        USERS_DB[user.id] = user_data
        return user
    
    def _dict_to_user(self, user_data: Dict[str, Any]) -> User:
        """Convierte un diccionario a entidad User."""
        return User(
            id=user_data["id"],
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"],
            role=Role(user_data["role"]),
            is_active=user_data.get("is_active", True)
        )


class TokenRepositoryImpl(TokenRepository):
    """Implementación en memoria del repositorio de tokens."""
    
    def save_token(self, token: Token) -> Token:
        """Guarda un token."""
        token_data = {
            "id": token.id,
            "user_id": token.user_id,
            "token_value": token.token_value,
            "token_type": token.token_type.value,
            "expires_at": token.expires_at.isoformat(),
            "created_at": token.created_at.isoformat(),
            "status": token.status.value,
            "permissions": token.permissions
        }
        TOKENS_DB[token.id] = token_data
        return token
    
    def find_token_by_value(self, token_value: str) -> Optional[Token]:
        """Busca un token por su valor."""
        for token_data in TOKENS_DB.values():
            if token_data["token_value"] == token_value:
                return self._dict_to_token(token_data)
        return None
    
    def find_active_tokens_by_user(self, user_id: str) -> list[Token]:
        """Busca todos los tokens activos de un usuario."""
        tokens = []
        for token_data in TOKENS_DB.values():
            if (token_data["user_id"] == user_id and 
                token_data["status"] == TokenStatus.ACTIVE.value):
                tokens.append(self._dict_to_token(token_data))
        return tokens
    
    def revoke_token(self, token_id: str) -> bool:
        """Revoca un token."""
        if token_id in TOKENS_DB:
            TOKENS_DB[token_id]["status"] = TokenStatus.REVOKED.value
            return True
        return False
    
    def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoca todos los tokens de un usuario."""
        count = 0
        for token_data in TOKENS_DB.values():
            if (token_data["user_id"] == user_id and 
                token_data["status"] == TokenStatus.ACTIVE.value):
                token_data["status"] = TokenStatus.REVOKED.value
                count += 1
        return count
    
    def _dict_to_token(self, token_data: Dict[str, Any]) -> Token:
        """Convierte un diccionario a entidad Token."""
        return Token(
            id=token_data["id"],
            user_id=token_data["user_id"],
            token_value=token_data["token_value"],
            token_type=TokenType(token_data["token_type"]),
            expires_at=datetime.fromisoformat(token_data["expires_at"]),
            created_at=datetime.fromisoformat(token_data["created_at"]),
            status=TokenStatus(token_data["status"]),
            permissions=token_data.get("permissions")
        )


class SessionRepositoryImpl(SessionRepository):
    """Implementación en memoria del repositorio de sesiones."""
    
    def save_session(self, session: Session) -> Session:
        """Guarda una sesión."""
        session_data = {
            "id": session.id,
            "user_id": session.user_id,
            "token": session.token,
            "expires_at": session.expires_at.isoformat()
        }
        SESSIONS_DB[session.id] = session_data
        return session
    
    def find_session_by_token(self, token: str) -> Optional[Session]:
        """Busca una sesión por token."""
        for session_data in SESSIONS_DB.values():
            if session_data["token"] == token:
                return self._dict_to_session(session_data)
        return None
    
    def delete_session(self, session_id: str) -> bool:
        """Elimina una sesión."""
        if session_id in SESSIONS_DB:
            del SESSIONS_DB[session_id]
            return True
        return False
    
    def _dict_to_session(self, session_data: Dict[str, Any]) -> Session:
        """Convierte un diccionario a entidad Session."""
        return Session(
            id=session_data["id"],
            user_id=session_data["user_id"],
            token=session_data["token"],
            expires_at=datetime.fromisoformat(session_data["expires_at"])
        )