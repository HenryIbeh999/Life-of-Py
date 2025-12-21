from scripts.jobs import load_jobs
import pygame
from sqlalchemy import *
from sqlalchemy.orm import *
from subclass.pop_up_panel import PopupPanel
from pathlib import Path
from sqlalchemy import create_engine
from scripts.path_utils import get_resource_path, get_save_path

db_path = Path(get_save_path("achievements.db"))

engine = create_engine(f"sqlite+pysqlite:///{db_path.as_posix()}", future=True)

class Base(DeclarativeBase):
    pass

class Achievement(Base):
    __tablename__ = "player_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    money_made: Mapped[float] = mapped_column(Float)
    money_spent: Mapped[float] = mapped_column(Float)
    taxes_paid: Mapped[float] = mapped_column(Float)
    days_lived : Mapped[int]
    jobs_had : Mapped[int]
    level: Mapped[int]

try:
    Base.metadata.create_all(engine)
except Exception as e:
    raise RuntimeError(f"Could not open or create database at {db_path}: {e}") from e

def save_achievement(game):
    with Session(engine) as session:
        existing = session.execute(select(Achievement).where(Achievement.name==game.player.name)).scalar()

        if not existing:
            new_achievement = Achievement(
                name = game.player.name,
                money_made = 0,
                money_spent = 0,
                taxes_paid = 0,
                days_lived = 1,
                jobs_had = 0,
                level = 1,

            )
        else:
            new_achievement = Achievement(
                name=game.player.name,
                money_made=round(game.achievement.money_made,2),
                money_spent=round(game.achievement.money_spent,2),
                taxes_paid=round(game.achievement.taxes_paid,2),
                days_lived=game.achievement.days_lived,
                jobs_had=game.achievement.jobs_had,
                level=game.achievement.level,

            )
        session.execute(delete(Achievement).where(Achievement.name==game.player.name))
        session.add(new_achievement)
        session.commit()


def load_achievement(game):
    with Session(engine) as session:
        row = session.execute(select(Achievement).where(Achievement.name==game.player.name)).scalar()
    return row

def delete_achievement(name):
    with Session(engine) as session:
        row = session.execute(select(Achievement).where(Achievement.name==name)).scalar()
        session.delete(row)
        session.commit()