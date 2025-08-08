from typing import List, Optional

from sqlalchemy.orm import Session

from ..database import FirearmDB, get_db
from ..models.firearm import ActionType, Caliber, Firearm, FirearmType, ModelType
from .firearm_repository import FirearmRepository


class DbFirearmRepository(FirearmRepository):
    def __init__(self, db_session: Optional[Session] = None):
        self.db_session = db_session
        self._sample_data_initialized = False

    def _get_db(self) -> Session:
        if self.db_session:
            return self.db_session
        return next(get_db())

    def _ensure_sample_data(self) -> None:
        if self._sample_data_initialized:
            return

        try:
            db = self._get_db()

            if db.query(FirearmDB).count() > 0:
                if not self.db_session:
                    db.close()
                self._sample_data_initialized = True
                return

            print("Loading sample firearm data...")

            sample_firearms = [
                FirearmDB(
                    id="ak47",
                    name="AK-47",
                    manufacturer="Kalashnikov Concern",
                    type=FirearmType.RIFLE.value,
                    caliber=Caliber.SEVEN_SIX_TWO_X39.value,
                    country_of_origin="Soviet Union",
                    model_type=ModelType.MILITARY.value,
                    year_introduced=1947,
                    action_type=ActionType.LONG_STROKE_GAS_PISTON.value,
                    description="Selective-fire assault rifle",
                    image_url="/uploads/images/ak47.jpg",
                ),
                FirearmDB(
                    id="mp40",
                    name="MP 40",
                    manufacturer="Erma Werke",
                    type=FirearmType.SMG.value,
                    caliber=Caliber.NINE_MM.value,
                    country_of_origin="Germany",
                    model_type=ModelType.MILITARY.value,
                    year_introduced=1940,
                    action_type=ActionType.SIMPLE_BLOWBACK.value,
                    description="German submachine gun used in WWII",
                    image_url="/uploads/images/mp40.jpg",
                ),
                FirearmDB(
                    id="colt_1911",
                    name="Colt M1911",
                    manufacturer="Colt's Manufacturing Company",
                    type=FirearmType.PISTOL.value,
                    caliber=Caliber.FORTY_FIVE_ACP.value,
                    country_of_origin="United States",
                    model_type=ModelType.MILITARY.value,
                    year_introduced=1911,
                    action_type=ActionType.SHOT_RECOIL.value,
                    description="Semi-automatic pistol",
                    image_url="/uploads/images/colt_1911.jpg",
                ),
                FirearmDB(
                    id="thompson_m1928",
                    name="Thompson M1928",
                    manufacturer="Auto-Ordnance Corporation",
                    type=FirearmType.SMG.value,
                    caliber=Caliber.FORTY_FIVE_ACP.value,
                    country_of_origin="United States",
                    model_type=ModelType.MILITARY.value,
                    year_introduced=1928,
                    action_type=ActionType.SIMPLE_BLOWBACK.value,
                    description="Submachine gun known as Tommy Gun",
                    image_url="/uploads/images/thompson.jpg",
                ),
                FirearmDB(
                    id="lee_enfield",
                    name="Lee-Enfield",
                    manufacturer="Royal Small Arms Factory",
                    type=FirearmType.RIFLE.value,
                    caliber=Caliber.THREE_OH_THREE_BRITISH.value,
                    country_of_origin="United Kingdom",
                    model_type=ModelType.MILITARY.value,
                    year_introduced=1895,
                    action_type=ActionType.ROTATING_BOLT_ACTION.value,
                    description="Bolt-action rifle used by British forces",
                    image_url="/uploads/images/lee_enfield.jpg",
                ),
                FirearmDB(
                    id="m1_garand",
                    name="M1 Garand",
                    manufacturer="Springfield Armory",
                    type=FirearmType.RIFLE.value,
                    caliber=Caliber.THIRTY_OH_SIX.value,
                    country_of_origin="United States",
                    model_type=ModelType.MILITARY.value,
                    year_introduced=1936,
                    action_type=ActionType.ROTATING_BOLT_ACTION.value,
                    description=("Semi-automatic rifle used by US forces in WWII"),
                    image_url="/uploads/images/m1_garand.jpg",
                ),
            ]

            for firearm_db in sample_firearms:
                db.add(firearm_db)

            db.commit()
            print(f"Loaded {len(sample_firearms)} sample firearms")

            if not self.db_session:
                db.close()

            self._sample_data_initialized = True

        except Exception as e:
            print(f"Error loading sample data: {e}")
            if not self.db_session and "db" in locals():
                db.close()

    def _db_to_pydantic(self, firearm_db: FirearmDB) -> Firearm:
        return Firearm(
            id=str(firearm_db.id),
            name=str(firearm_db.name),
            manufacturer=str(firearm_db.manufacturer),
            type=FirearmType(str(firearm_db.type)),
            caliber=Caliber(str(firearm_db.caliber)),
            country_of_origin=str(firearm_db.country_of_origin),
            model_type=ModelType(str(firearm_db.model_type)),
            action_type=ActionType(str(firearm_db.action_type)),
            year_introduced=int(firearm_db.year_introduced),
            description=str(firearm_db.description),
            image_url=str(firearm_db.image_url),
        )

    def _pydantic_to_db(self, firearm: Firearm) -> FirearmDB:
        return FirearmDB(
            id=firearm.id,
            name=firearm.name,
            manufacturer=firearm.manufacturer,
            type=firearm.type.value,
            caliber=firearm.caliber.value,
            country_of_origin=firearm.country_of_origin,
            model_type=firearm.model_type.value,
            year_introduced=firearm.year_introduced,
            action_type=firearm.action_type.value,
            description=firearm.description,
            image_url=firearm.image_url,
        )

    def get_all_firearms(self) -> List[Firearm]:
        try:
            self._ensure_sample_data()
            db = self._get_db()
            firearms_db = db.query(FirearmDB).all()
            result = [self._db_to_pydantic(f) for f in firearms_db]

            if not self.db_session:
                db.close()
            return result
        except Exception as e:
            print(f"Error getting firearms: {e}")
            return []

    def get_firearm_by_id(self, firearm_id: str) -> Optional[Firearm]:
        try:
            self._ensure_sample_data()
            db = self._get_db()
            firearm_db = db.query(FirearmDB).filter(FirearmDB.id == firearm_id).first()

            result = None
            if firearm_db:
                result = self._db_to_pydantic(firearm_db)

            if not self.db_session:
                db.close()
            return result
        except Exception as e:
            print(f"Error getting firearm {firearm_id}: {e}")
            return None

    def add_firearm(self, firearm: Firearm) -> bool:
        try:
            self._ensure_sample_data()
            db = self._get_db()

            existing = db.query(FirearmDB).filter(FirearmDB.id == firearm.id).first()
            if existing:
                if not self.db_session:
                    db.close()
                return False

            firearm_db = self._pydantic_to_db(firearm)
            db.add(firearm_db)
            db.commit()

            if not self.db_session:
                db.close()
            return True

        except Exception as e:
            print(f"Error adding firearm: {e}")
            return False

    def update_firearm(self, firearm_id: str, firearm: Firearm) -> bool:
        try:
            self._ensure_sample_data()
            db = self._get_db()

            firearm_db = db.query(FirearmDB).filter(FirearmDB.id == firearm_id).first()
            if not firearm_db:
                if not self.db_session:
                    db.close()
                return False

            setattr(firearm_db, "name", firearm.name)
            setattr(firearm_db, "manufacturer", firearm.manufacturer)
            setattr(firearm_db, "type", firearm.type.value)
            setattr(firearm_db, "caliber", firearm.caliber.value)
            setattr(firearm_db, "country_of_origin", firearm.country_of_origin)
            setattr(firearm_db, "model_type", firearm.model_type.value)
            setattr(firearm_db, "year_introduced", firearm.year_introduced)
            setattr(firearm_db, "description", firearm.description)
            setattr(firearm_db, "action_type", firearm.action_type.value)
            setattr(firearm_db, "image_url", firearm.image_url)

            db.commit()
            if not self.db_session:
                db.close()
            return True

        except Exception as e:
            print(f"Error updating firearm: {e}")
            return False

    def delete_firearm(self, firearm_id: str) -> bool:
        try:
            self._ensure_sample_data()
            db = self._get_db()

            firearm_db = db.query(FirearmDB).filter(FirearmDB.id == firearm_id).first()
            if not firearm_db:
                if not self.db_session:
                    db.close()
                return False

            db.delete(firearm_db)
            db.commit()

            if not self.db_session:
                db.close()
            return True

        except Exception as e:
            print(f"Error deleting firearm: {e}")
            return False

    def firearm_exists(self, firearm_id: str) -> bool:
        try:
            self._ensure_sample_data()
            db = self._get_db()
            exists = (
                db.query(FirearmDB).filter(FirearmDB.id == firearm_id).first()
                is not None
            )

            if not self.db_session:
                db.close()
            return exists
        except Exception as e:
            print(f"Error checking firearm existence: {e}")
            return False
