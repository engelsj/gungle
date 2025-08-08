from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.firearm import Firearm


class FirearmRepository(ABC):
    @abstractmethod
    def get_all_firearms(self) -> List[Firearm]:
        pass

    @abstractmethod
    def get_firearm_by_id(self, firearm_id: str) -> Optional[Firearm]:
        pass

    @abstractmethod
    def firearm_exists(self, firearm_id: str) -> bool:
        pass

    @abstractmethod
    def add_firearm(self, firearm: Firearm) -> bool:
        pass

    @abstractmethod
    def update_firearm(self, firearm_id: str, firearm: Firearm) -> bool:
        pass

    @abstractmethod
    def delete_firearm(self, firearm_id: str) -> bool:
        pass
