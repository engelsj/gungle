from typing import Dict, List, Optional

from ..models.firearm import AdoptionStatus, Firearm, FirearmType


class FirearmService:
    def __init__(self) -> None:
        self._firearms: Dict[str, Firearm] = {}
        self._load_sample_data()

    def _load_sample_data(self) -> None:
        sample_firearms = [
            {
                "id": "m1_garand",
                "name": "M1 Garand",
                "manufacturer": "Springfield Armory",
                "type": FirearmType.RIFLE,
                "caliber": ".30-06 Springfield",
                "country_of_origin": "United States",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1936,
                "action_type": "TODO",
                "image_url": "/uploads/images/m1_garand.jpg",
            },
            {
                "id": "ak47",
                "name": "AK-47",
                "manufacturer": "Kalashnikov Concern",
                "type": FirearmType.RIFLE,
                "caliber": "7.62×39mm",
                "country_of_origin": "Soviet Union",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1947,
                "action_type": "TODO",
                "image_url": "/uploads/images/ak47.jpg",
            },
            {
                "id": "mp40",
                "name": "MP 40",
                "manufacturer": "Erma Werke",
                "type": FirearmType.SMG,
                "caliber": "9×19mm Parabellum",
                "country_of_origin": "Germany",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1940,
                "action_type": "TODO",
                "image_url": "/uploads/images/mp40.jpg",
            },
            {
                "id": "colt_1911",
                "name": "Colt M1911",
                "manufacturer": "Colt's Manufacturing Company",
                "type": FirearmType.PISTOL,
                "caliber": ".45 ACP",
                "country_of_origin": "United States",
                "adoption_status": AdoptionStatus.BOTH,
                "year_introduced": 1911,
                "action_type": "TODO",
                "image_url": "/uploads/images/colt_1911.jpg",
            },
            {
                "id": "thompson_m1928",
                "name": "Thompson M1928",
                "manufacturer": "Auto-Ordnance Corporation",
                "type": FirearmType.SMG,
                "caliber": ".45 ACP",
                "country_of_origin": "United States",
                "adoption_status": AdoptionStatus.BOTH,
                "year_introduced": 1928,
                "action_type": "TODO",
                "image_url": "/uploads/images/thompson.jpg",
            },
            {
                "id": "lee_enfield",
                "name": "Lee-Enfield",
                "manufacturer": "Royal Small Arms Factory",
                "type": FirearmType.RIFLE,
                "caliber": ".303 British",
                "country_of_origin": "United Kingdom",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1895,
                "action_type": "TODO",
                "image_url": "/uploads/images/lee_enfield.jpg",
            },
            {
                "id": "kar98k",
                "name": "Karabiner 98k",
                "manufacturer": "Mauser",
                "type": FirearmType.RIFLE,
                "caliber": "7.92×57mm Mauser",
                "country_of_origin": "Germany",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1935,
                "action_type": "TODO",
                "image_url": "/uploads/images/kar98k.jpg",
            },
            {
                "id": "mosin_nagant",
                "name": "Mosin-Nagant",
                "manufacturer": "Tula Arms Plant",
                "type": FirearmType.RIFLE,
                "caliber": "7.62×54mmR",
                "country_of_origin": "Russia",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1891,
                "action_type": "TODO",
                "image_url": "/uploads/images/mosin_nagant.jpg",
            },
            {
                "id": "stg44",
                "name": "StG 44",
                "manufacturer": "C.G. Haenel",
                "type": FirearmType.RIFLE,
                "caliber": "7.92×33mm Kurz",
                "country_of_origin": "Germany",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1943,
                "action_type": "TODO",
                "image_url": "/uploads/images/stg44.jpg",
            },
            {
                "id": "m16",
                "name": "M16",
                "manufacturer": "Colt",
                "type": FirearmType.RIFLE,
                "caliber": "5.56×45mm NATO",
                "country_of_origin": "United States",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1964,
                "action_type": "TODO",
                "image_url": "/uploads/images/m16.jpg",
            },
            {
                "id": "uzi",
                "name": "Uzi",
                "manufacturer": "Israel Military Industries",
                "type": FirearmType.SMG,
                "caliber": "9×19mm Parabellum",
                "country_of_origin": "Israel",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1954,
                "action_type": "TODO",
                "image_url": "/uploads/images/uzi.jpg",
            },
            {
                "id": "ppsh41",
                "name": "PPSh-41",
                "manufacturer": "Soviet Union",
                "type": FirearmType.SMG,
                "caliber": "7.62×25mm Tokarev",
                "country_of_origin": "Soviet Union",
                "adoption_status": AdoptionStatus.MILITARY,
                "year_introduced": 1941,
                "action_type": "TODO",
                "image_url": "/uploads/images/ppsh41.jpg",
            },
        ]

        for firearm_data in sample_firearms:
            firearm = Firearm(**firearm_data)
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
