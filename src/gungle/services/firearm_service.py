from typing import Dict, List, Optional

from ..models.firearm import AdoptionStatus, Firearm, FirearmType


class FirearmService:
    def __init__(self) -> None:
        self._firearms: Dict[str, Firearm] = {}
        self._load_sample_data()

    def _load_sample_data(self) -> None:
        sample_firearms = [
            Firearm(
                id="m1_garand",
                name="M1 Garand",
                manufacturer="Springfield Armory",
                type=FirearmType.RIFLE,
                caliber=".30-06 Springfield",
                country_of_origin="United States",
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1936,
                actionType="Gas-operated, closed rotating bolt",
                description="Semi-automatic rifle used by US forces in WWII",
                image_url="/uploads/images/m1_garand.jpg",
            ),
            Firearm(
                id="ak47",
                name="AK-47",
                manufacturer="Kalashnikov Concern",
                type=FirearmType.RIFLE,
                caliber="7.62×39mm",
                country_of_origin="Soviet Union",
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1947,
                actionType="long-stroke piston",
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
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1940,
                actionType="Open bolt blowback",
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
                adoption_status=AdoptionStatus.BOTH,
                year_introduced=1911,
                actionType="Recoil Operated",
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
                adoption_status=AdoptionStatus.BOTH,
                year_introduced=1928,
                actionType="Open bolt blowback",
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
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1895,
                actionType="Bolt action",
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
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1935,
                actionType="Bolt action",
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
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1891,
                actionType="Bolt action",
                description="Bolt-action rifle used by Russian forces",
                image_url="/uploads/images/mosin_nagant.jpg",
            ),
            Firearm(
                id="stg44",
                name="StG 44",
                manufacturer="C.G. Haenel",
                type=FirearmType.RIFLE,
                caliber="7.92×33mm Kurz",
                country_of_origin="Germany",
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1943,
                actionType="Gas-operated tilting bolt",
                description="First modern assault rifle",
                image_url="/uploads/images/stg44.jpg",
            ),
            Firearm(
                id="m16",
                name="M16",
                manufacturer="Colt",
                type=FirearmType.RIFLE,
                caliber="5.56×45mm NATO",
                country_of_origin="United States",
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1964,
                actionType="Gas-operated rotating bolt",
                description="American assault rifle used in Vietnam War",
                image_url="/uploads/images/m16.jpg",
            ),
            Firearm(
                id="uzi",
                name="Uzi",
                manufacturer="Israel Military Industries",
                type=FirearmType.SMG,
                caliber="9×19mm Parabellum",
                country_of_origin="Israel",
                adoption_status=AdoptionStatus.BOTH,
                year_introduced=1954,
                actionType="Open bolt blowback",
                description="Israeli submachine gun",
                image_url="/uploads/images/uzi.jpg",
            ),
            Firearm(
                id="ppsh41",
                name="PPSh-41",
                manufacturer="Soviet Union",
                type=FirearmType.SMG,
                caliber="7.62×25mm Tokarev",
                country_of_origin="Soviet Union",
                adoption_status=AdoptionStatus.MILITARY,
                year_introduced=1941,
                actionType="Open bolt blowback",
                description="Soviet submachine gun used in WWII",
                image_url="/uploads/images/ppsh41.jpg",
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
