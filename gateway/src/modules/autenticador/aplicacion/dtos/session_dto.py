from dataclasses import dataclass

from datetime import datetime

@dataclass(frozen=True)
class SessionDto:
    id: str
    user_id: str
    token: str
    expires_at: datetime