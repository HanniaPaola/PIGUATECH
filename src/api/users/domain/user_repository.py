from abc import ABC, abstractmethod
from typing import Optional, List
from .user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def list_acuicultores_by_supervisor(self, supervisor_id: int) -> List[User]:
        pass
