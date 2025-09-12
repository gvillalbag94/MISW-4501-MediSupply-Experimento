from datetime import datetime, timedelta
from modules.autenticador.dominio.entities.session import Session
from modules.autenticador.aplicacion.mappers.session_mapper import SessionMapper
from modules.autenticador.aplicacion.dtos.session_dto import SessionDto
from modules.autenticador.dominio.entities.user import User, Role
from modules.autenticador.dominio.repositorios.auth_repository import AuthRepository
import jwt

user = User(
    id="1",
    name="John Doe",
    email="john.doe@example.com",
    password="User1234*",
    role=Role.USER,
)

admin = User(
    id="2",
    name="Admin Doe",
    email="admin.doe@example.com",
    password="Admin1234*",
    role=Role.ADMIN,
)

users = [user, admin]

class AuthService:
    def __init__(self, auth_repository: AuthRepository, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.auth_repository = auth_repository

    def login(self, email: str, password: str) -> SessionDto:
        try:
            auth = next((user for user in users if user.email == email and user.password == password), None)
            if auth:
                exp = datetime.now() + timedelta(hours=1)
                token = jwt.encode(
                    {"user_id": auth.id, "role": auth.role.value, "exp": exp},
                    key=self.secret_key,
                    algorithm=self.algorithm
                )
                session = Session(
                    id=auth.id,
                    user_id=auth.id,
                    token=token,
                    expires_at=exp,
                )
                return SessionMapper.entity_to_dto(session)
            else:   
                return None 
        except Exception as e:
            return None