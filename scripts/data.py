from scripts.jobs import load_jobs
from pygame_gui.elements import UIButton
import pygame
from pygame_gui.core import ObjectID
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.exc import IntegrityError
from subclass.pop_up_panel import PopupPanel

engine = create_engine("sqlite+pysqlite:///save.db")

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "player_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30),unique=True)
    money: Mapped[float] = mapped_column(Float)
    health: Mapped[int]
    energy : Mapped[int]
    hunger : Mapped[int]
    job : Mapped[str] = mapped_column(String(50),nullable=True)
    deposit : Mapped[float] = mapped_column(Float)
    day : Mapped[int]


Base.metadata.create_all(engine)

def save_game(player,name,menu):
    if player.name == "":
        player.name = name
    new_save = Player(
        name = player.name,
        money = player.money,
        health = player.health,
        energy = player.energy,
        hunger = player.hunger,
        job = player.job.name if player.job else None,
        deposit=player.deposit,
        day = player.day
    )

    with Session(engine) as session:
        session.execute(delete(Player).where(Player.name==player.name))
        session.commit()
        try:
            session.add(new_save)
            session.commit()
        except IntegrityError:
            PopupPanel.show_message(manager=menu.manager, text="Save name already exist!",screen_size=menu.screen.get_size())


def overwrite_save(player,old_name):
    new_save = Player(
        name = player.name,
        money = player.money,
        health = player.health,
        energy = player.energy,
        hunger = player.hunger,
        job = player.job.name if player.job else None,
        deposit = player.deposit,
        day = player.day
    )

    with Session(engine) as session:
        session.execute(delete(Player).where(Player.name==old_name))
        session.commit()
        session.add(new_save)
        session.commit()

def load_game(player,name):
    with Session(engine) as session:
        loaded_save = session.execute(select(Player).where(Player.name==name))
        row = loaded_save.scalar()
        jobs = load_jobs()
        if row:
            player.name = row.name,
            player.money = row.money
            player.health = row.health
            player.energy = row.energy
            player.hunger = row.hunger
            player.job = next((j for j in jobs if j.name == row.job), None)
            player.deposit = row.deposit
            player.day = row.day
            return player
        return None

def delete_save(name):
    with Session(engine) as session:
        session.execute(delete(Player).where(Player.name==name))
        session.commit()


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
                                          object_id=ObjectID(class_id='@small_button', object_id='#menu_load_button'),
                                          container=menu.load_panel))
            return save_list[:3]

    except FileNotFoundError:
        return None

