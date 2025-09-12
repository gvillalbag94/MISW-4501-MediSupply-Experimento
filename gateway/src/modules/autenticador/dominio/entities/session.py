from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

@dataclass(frozen=True)
class Session:
    id: str
    user_id: str
    token: str
    expires_at: datetime

    @staticmethod
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at,
        }