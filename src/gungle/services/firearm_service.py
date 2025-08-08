from typing import List, Optional

from ..models.firearm import Firearm
from ..repositories.db_firearm_repository import DbFirearmRepository
from ..repositories.firearm_repository import FirearmRepository


class FirearmService:
    def __init__(self, repository: Optional[FirearmRepository] = None):
        self.repository = repository or DbFirearmRepository()

    def get_all_firearms(self) -> List[Firearm]:
        return self.repository.get_all_firearms()

    def get_firearm_by_id(self, firearm_id: str) -> Optional[Firearm]:
        return self.repository.get_firearm_by_id(firearm_id)

    def add_firearm(self, firearm: Firearm) -> bool:
        return self.repository.add_firearm(firearm)

    def update_firearm(self, firearm_id: str, firearm: Firearm) -> bool:
        return self.repository.update_firearm(firearm_id, firearm)

    def delete_firearm(self, firearm_id: str) -> bool:
        return self.repository.delete_firearm(firearm_id)

    def firearm_exists(self, firearm_id: str) -> bool:
        return self.repository.firearm_exists(firearm_id)


firearm_service = FirearmService()
