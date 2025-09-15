from abc import ABC, abstractmethod
from typing import Optional
from ..entities import User, Token, Session


class AuthRepository(ABC):
    """Repositorio abstracto para operaciones de autenticación y autorización."""
    
    @abstractmethod
    def find_user_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por email."""
        pass
    
    @abstractmethod
    def find_user_by_id(self, user_id: str) -> Optional[User]:
        """Busca un usuario por ID."""
        pass
    
    @abstractmethod
    def save_user(self, user: User) -> User:
        """Guarda un usuario."""
        pass


class TokenRepository(ABC):
    """Repositorio abstracto para operaciones con tokens."""
    
    @abstractmethod
    def save_token(self, token: Token) -> Token:
        """Guarda un token."""
        pass
    
    @abstractmethod
    def find_token_by_value(self, token_value: str) -> Optional[Token]:
        """Busca un token por su valor."""
        pass
    
    @abstractmethod
    def find_active_tokens_by_user(self, user_id: str) -> list[Token]:
        """Busca todos los tokens activos de un usuario."""
        pass
    
    @abstractmethod
    def revoke_token(self, token_id: str) -> bool:
        """Revoca un token."""
        pass
    
    @abstractmethod
    def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoca todos los tokens de un usuario."""
        pass


class SessionRepository(ABC):
    """Repositorio abstracto para operaciones con sesiones."""
    
    @abstractmethod
    def save_session(self, session: Session) -> Session:
        """Guarda una sesión."""
        pass
    
    @abstractmethod
    def find_session_by_token(self, token: str) -> Optional[Session]:
        """Busca una sesión por token."""
        pass
    
    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """Elimina una sesión."""
        pass