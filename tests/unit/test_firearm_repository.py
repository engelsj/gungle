from typing import List, Optional

from ...src.gungle.models.firearm import (
    ActionType,
    Caliber,
    Firearm,
    FirearmType,
    ModelType,
)
from ...src.gungle.repositories.firearm_repository import FirearmRepository


class TestFirearmRepository(FirearmRepository):
    def __init__(self) -> None:
        self._firearms = self._create_sample_data()

    def _create_sample_data(self) -> List[Firearm]:
        return [
            Firearm(
                id="ak47",
                name="AK-47",
                manufacturer="Kalashnikov Concern",
                type=FirearmType.RIFLE,
                caliber=Caliber.SEVEN_SIX_TWO_X39,
                country_of_origin="Soviet Union",
                model_type=ModelType.MILITARY,
                year_introduced=1947,
                action_type=ActionType.LONG_STROKE_GAS_PISTON,
                description="Selective-fire assault rifle",
                image_url="/uploads/images/ak47.jpg",
            ),
            Firearm(
                id="mp40",
                name="MP 40",
                manufacturer="Erma Werke",
                type=FirearmType.SMG,
                caliber=Caliber.NINE_MM,
                country_of_origin="Germany",
                model_type=ModelType.MILITARY,
                year_introduced=1940,
                action_type=ActionType.SIMPLE_BLOWBACK,
                description="German submachine gun used in WWII",
                image_url="/uploads/images/mp40.jpg",
            ),
            Firearm(
                id="colt_1911",
                name="Colt M1911",
                manufacturer="Colt's Manufacturing Company",
                type=FirearmType.PISTOL,
                caliber=Caliber.FORTY_FIVE_ACP,
                country_of_origin="United States",
                model_type=ModelType.MILITARY,
                year_introduced=1911,
                action_type=ActionType.SHOT_RECOIL,
                description="Semi-automatic pistol",
                image_url="/uploads/images/colt_1911.jpg",
            ),
            Firearm(
                id="thompson_m1928",
                name="Thompson M1928",
                manufacturer="Auto-Ordnance Corporation",
                type=FirearmType.SMG,
                caliber=Caliber.FORTY_FIVE_ACP,
                country_of_origin="United States",
                model_type=ModelType.MILITARY,
                year_introduced=1928,
                action_type=ActionType.SIMPLE_BLOWBACK,
                description="Submachine gun known as Tommy Gun",
                image_url="/uploads/images/thompson.jpg",
            ),
            Firearm(
                id="lee_enfield",
                name="Lee-Enfield",
                manufacturer="Royal Small Arms Factory",
                type=FirearmType.RIFLE,
                caliber=Caliber.THREE_OH_THREE_BRITISH,
                country_of_origin="United Kingdom",
                model_type=ModelType.MILITARY,
                year_introduced=1895,
                action_type=ActionType.ROTATING_BOLT_ACTION,
                description="Bolt-action rifle used by British forces",
                image_url="/uploads/images/lee_enfield.jpg",
            ),
            Firearm(
                id="m1_garand",
                name="M1 Garand",
                manufacturer="Springfield Armory",
                type=FirearmType.RIFLE,
                caliber=Caliber.THIRTY_OH_SIX,
                country_of_origin="United States",
                model_type=ModelType.MILITARY,
                year_introduced=1936,
                action_type=ActionType.ROTATING_BOLT_ACTION,
                description="Semi-automatic rifle used by US forces in WWII",
                image_url="/uploads/images/m1_garand.jpg",
            ),
        ]

    def get_all_firearms(self) -> List[Firearm]:
        return self._firearms.copy()

    def get_firearm_by_id(self, firearm_id: str) -> Optional[Firearm]:
        return next((f for f in self._firearms if f.id == firearm_id), None)

    def firearm_exists(self, firearm_id: str) -> bool:
        return any(f.id == firearm_id for f in self._firearms)

    def add_firearm(self, firearm: Firearm) -> bool:
        if self.firearm_exists(firearm.id):
            return False
        self._firearms.append(firearm)
        return True

    def update_firearm(self, firearm_id: str, firearm: Firearm) -> bool:
        for i, f in enumerate(self._firearms):
            if f.id == firearm_id:
                self._firearms[i] = firearm
                return True
        return False

    def delete_firearm(self, firearm_id: str) -> bool:
        for i, f in enumerate(self._firearms):
            if f.id == firearm_id:
                del self._firearms[i]
                return True
        return False
