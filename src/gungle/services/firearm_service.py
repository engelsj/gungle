from typing import Dict, List, Optional

from ..models.firearm import ActionType, Firearm, FirearmType, ModelType


class FirearmService:
    def __init__(self) -> None:
        self._firearms: Dict[str, Firearm] = {}
        self._load_sample_data()

    def _load_sample_data(self) -> None:
        sample_firearms = [
            Firearm(
                id="ak47",
                name="AK-47",
                manufacturer="Kalashnikov Concern",
                type=FirearmType.RIFLE,
                caliber="7.62×39mm",
                country_of_origin="Soviet Union",
                model_type=ModelType.MILITARY,
                year_introduced=1947,
                actionType=ActionType.LONG_STROKE_GAS_PISTON,
                description="Selective-fire assault rifle",
                image_url="/uploads/images/ak47.jpg",
            ),
            Firearm(
                id="mp40",
                name="MP 40",
                manufacturer="Erma Werke",
                type=FirearmType.SMG,
                caliber="9×19mm Parabellum",
                country_of_origin="Germany",
                model_type=ModelType.MILITARY,
                year_introduced=1940,
                actionType=ActionType.SIMPLE_BLOWBACK,
                description="German submachine gun used in WWII",
                image_url="/uploads/images/mp40.jpg",
            ),
            Firearm(
                id="colt_1911",
                name="Colt M1911",
                manufacturer="Colt's Manufacturing Company",
                type=FirearmType.PISTOL,
                caliber=".45 ACP",
                country_of_origin="United States",
                model_type=ModelType.MILITARY,
                year_introduced=1911,
                actionType=ActionType.SHOT_RECOIL,
                description="Semi-automatic pistol",
                image_url="/uploads/images/colt_1911.jpg",
            ),
            Firearm(
                id="thompson_m1928",
                name="Thompson M1928",
                manufacturer="Auto-Ordnance Corporation",
                type=FirearmType.SMG,
                caliber=".45 ACP",
                country_of_origin="United States",
                model_type=ModelType.MILITARY,
                year_introduced=1928,
                actionType=ActionType.SIMPLE_BLOWBACK,
                description="Submachine gun known as Tommy Gun",
                image_url="/uploads/images/thompson.jpg",
            ),
            Firearm(
                id="lee_enfield",
                name="Lee-Enfield",
                manufacturer="Royal Small Arms Factory",
                type=FirearmType.RIFLE,
                caliber=".303 British",
                country_of_origin="United Kingdom",
                model_type=ModelType.MILITARY,
                year_introduced=1895,
                actionType=ActionType.ROTATING_BOLT_ACTION,
                description="Bolt-action rifle used by British forces",
                image_url="/uploads/images/lee_enfield.jpg",
            ),
            Firearm(
                id="kar98k",
                name="Karabiner 98k",
                manufacturer="Mauser",
                type=FirearmType.RIFLE,
                caliber="7.92×57mm Mauser",
                country_of_origin="Germany",
                model_type=ModelType.MILITARY,
                year_introduced=1935,
                actionType=ActionType.ROTATING_BOLT_ACTION,
                description="German bolt-action rifle",
                image_url="/uploads/images/kar98k.jpg",
            ),
            Firearm(
                id="mosin_nagant",
                name="Mosin-Nagant",
                manufacturer="Tula Arms Plant",
                type=FirearmType.RIFLE,
                caliber="7.62×54mmR",
                country_of_origin="Russia",
                model_type=ModelType.MILITARY,
                year_introduced=1891,
                actionType=ActionType.ROTATING_BOLT_ACTION,
                description="Bolt-action rifle used by Russian forces",
                image_url="/uploads/images/mosin_nagant.jpg",
            ),
        ]

        for firearm in sample_firearms:
            self._firearms[firearm.id] = firearm

    def get_all_firearms(self) -> List[Firearm]:
        return list(self._firearms.values())

    def get_firearm_by_id(self, firearm_id: str) -> Optional[Firearm]:
        return self._firearms.get(firearm_id)

    def add_firearm(self, firearm: Firearm) -> bool:
        if firearm.id in self._firearms:
            return False
        self._firearms[firearm.id] = firearm
        return True

    def update_firearm(self, firearm_id: str, firearm: Firearm) -> bool:
        if firearm_id not in self._firearms:
            return False
        self._firearms[firearm_id] = firearm
        return True

    def delete_firearm(self, firearm_id: str) -> bool:
        if firearm_id not in self._firearms:
            return False
        del self._firearms[firearm_id]
        return True

    def firearm_exists(self, firearm_id: str) -> bool:
        return firearm_id in self._firearms


firearm_service = FirearmService()
