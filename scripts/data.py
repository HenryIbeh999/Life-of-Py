from scripts.jobs import load_jobs
from pygame_gui.elements import UIButton
import pygame
from pygame_gui.core import ObjectID
from sqlalchemy import *
from sqlalchemy.orm import *
from subclass.pop_up_panel import PopupPanel
from pathlib import Path
from sqlalchemy import create_engine
from scripts.path_utils import get_resource_path, get_save_path

db_path = Path(get_save_path("save.db"))

engine = create_engine(f"sqlite+pysqlite:///{db_path.as_posix()}", future=True)

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "player_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    money: Mapped[float] = mapped_column(Float)
    health: Mapped[int]
    energy : Mapped[int]
    hunger : Mapped[int]
    job : Mapped[str] = mapped_column(String(50),nullable=True)
    deposit : Mapped[float] = mapped_column(Float)
    day : Mapped[int]
    gender: Mapped[int] = mapped_column(nullable=False)
    level: Mapped[int]
    level_progress: Mapped[int]

try:
    Base.metadata.create_all(engine)
except Exception as e:
    raise RuntimeError(f"Could not open or create database at {db_path}: {e}") from e

def save_game(player,name,menu):
    if player.name == "":
        player.name = name
    with Session(engine) as session:
        existing = session.scalar(select(Player).where(Player.name == player.name))
        try:
            if existing.name.split()[0] == name.split()[0]:
                PopupPanel.show_message(
                    manager=menu.manager,
                    text="Save Name Already Exists.",
                    screen_size=menu.window_surface.get_size(),
                    positive=False
                )
                return False
        except AttributeError:
            if existing:
                PopupPanel.show_message(
                    manager=menu.manager,
                    text="Save Name Already Exists.",
                    screen_size=menu.window_surface.get_size(),
                    positive=False
                )
                return False
        new_save = Player(
            name = player.name,
            money = player.money,
            health = player.health,
            energy = player.energy,
            hunger = player.hunger,
            job = player.job.name if player.job else None,
            deposit=player.deposit,
            day = player.day,
            gender = player.gender,
            level = player.level,
            level_progress = player.level_progress
        )
        session.add(new_save)
        session.commit()
        return True



# This is specifically for in-game save overwriting
def overwrite_save(player,old_name):
    new_save = Player(
        name = player.name,
        money = player.money,
        health = player.health,
        energy = player.energy,
        hunger = player.hunger,
        job = player.job.name if player.job else None,
        deposit = player.deposit,
        day = player.day,
        gender=player.gender,
        level=player.level,
        level_progress=player.level_progress
    )

    with Session(engine) as session:
        session.execute(delete(Player).where(Player.name==old_name))
        session.commit()
        session.add(new_save)
        session.commit()

def load_game(player,name):
    with Session(engine) as session:
        row = session.scalar(select(Player).where(Player.name == name))
        jobs = load_jobs()
        if row:
            player.name = row.name
            player.money = row.money
            player.health = row.health
            player.energy = row.energy
            player.hunger = row.hunger
            player.job = next((j for j in jobs if j.name == row.job), None)
            player.deposit = row.deposit
            player.day = row.day
            player.gender = row.gender
            player.level = row.level
            player.level_progress = row.level_progress
            return player
        return None

def delete_save(name):
    with Session(engine) as session:
        session.execute(delete(Player).where(Player.name==name))
        session.commit()

# I did this to display the save objects in the load menu
def query_save(menu):
    try:
        with Session(engine) as session:
            loaded_saves = session.execute(select(Player)).scalars()
            row = loaded_saves.fetchall()
            save_list = []
            menu.button_space = 0
            for save in row:
                menu.button_space += 70
                save_list.append(UIButton(relative_rect=pygame.Rect(0, menu.button_space, 200, 50), text=f"{save.name}",
                                          manager=menu.manager, anchors={'centerx': 'centerx'},
                                          object_id=ObjectID(class_id='@menu_button', object_id='#menu_load_button'),
                                          container=menu.load_panel))
            return save_list

    except FileNotFoundError:
        return None

