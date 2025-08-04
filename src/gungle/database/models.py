from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from .database import Base


class FirearmDB(Base):
    __tablename__ = "firearms"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    manufacturer = Column(String, nullable=False)
    type = Column(String, nullable=False)
    caliber = Column(String, nullable=False)
    country_of_origin = Column(String, nullable=False)
    model_type = Column(String, nullable=False)
    year_introduced = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    action_type = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class GameSessionDB(Base):
    __tablename__ = "game_sessions"
    session_id = Column(String, primary_key=True, index=True)
    target_firearm_id = Column(String, nullable=False)
    guesses_made = Column(Text, nullable=False)
    is_completed = Column(String, nullable=False)
    is_won = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    max_guesses = Column(Integer, default=5)
