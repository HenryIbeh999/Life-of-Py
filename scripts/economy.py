import pygame
from sqlalchemy import *
from sqlalchemy.orm import *
from subclass.pop_up_panel import PopupPanel
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import csv
import io
import seaborn as sns
import random

db_path = Path(__file__).resolve().parents[1] / "data" / "save" / "economy.db"
db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite+pysqlite:///{db_path.as_posix()}", future=True)


class Base(DeclarativeBase):
    pass

class Economy(Base):
    __tablename__ = "economy_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    inflation: Mapped[float]
    interest_rate: Mapped[float]
    salary_index: Mapped[float]
    tax_rate : Mapped[float]

try:
    Base.metadata.create_all(engine)
except Exception as e:
    raise RuntimeError(f"Could not open or create database at {db_path}: {e}") from e


def save_economy(game):
    with Session(engine) as session:
        if game.player.day == 1:
            new_economy = Economy(
                name=game.player.name,
                inflation = 1,
                interest_rate = 1,
                salary_index = 1,
                tax_rate = 1
            )

        elif game.economy:
            new_economy = Economy(
                name = game.player.name,
                inflation = round(game.economy.inflation,2),
                interest_rate = round(game.economy.interest_rate,2),
                salary_index = round(game.economy.salary_index,2),
                tax_rate = round(game.economy.tax_rate,2)
            )

        else:
            new_economy = Economy(
                name=game.player.name,
                inflation = 1,
                interest_rate = 1,
                salary_index = 1,
                tax_rate = 1
            )


        session.execute(delete(Economy).where(Economy.name==game.player.name))
        session.add(new_economy)
        session.commit()

def update_csv(game):
    csv_path = Path(__file__).resolve().parents[1] / "data" / "save" / f"{game.player.name.split()[0]}_economy.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    header = ['Day','Inflation','Interest Rate','Salary Index','Tax Rate']
    row = [
        int(game.player.day),
        round(game.economy.inflation,2),
        round(game.economy.interest_rate,2),
        round(game.economy.salary_index,2),
        round(game.economy.tax_rate,2),
    ]
    file_existed = csv_path.exists()
    with open(csv_path, mode='w' if game.player.day == 1 else 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        # file is new or empty -> write header first
        if not file_existed or csv_file.tell() == 0:
            writer.writerow(header)
            writer.writerow(row)

        else:
            try:
                df= pd.read_csv(csv_path)
                if df['Day'].tail(1) == game.player.day:
                    return None
            except ValueError:
                writer.writerow(row)


def load_economy(game):
    with Session(engine) as session:
        economy_data = session.execute(select(Economy).where(Economy.name==game.player.name)).scalar()
    return economy_data

def delete_economy(name):
    with Session(engine) as session:
        economy_data = session.execute(select(Economy).where(Economy.name==name)).scalar()
        session.delete(economy_data)
        session.commit()


def _random_adjust(value, min_value=0.1, max_value=100.0, max_pct_change=0.2):
    """
    Adjust value by a random discrete percent in [-max_pct_change, +max_pct_change].
    Result is rounded to two decimals and clamped to [min_value, max_value].
    """
    if value is None or value <= 0:
        value = min_value
    max_int = int(max_pct_change * 100)
    change_pct = random.randint(-max_int, max_int) / 100.0
    new = round(value * (1.0 + change_pct), 2)
    new = max(min_value, min(new, max_value))
    return float(new)



def advance_economy(game):
    game.economy.interest_rate = _random_adjust(
        game.economy.interest_rate, min_value=1.0, max_value=10.0, max_pct_change=0.5
    )

    game.economy.salary_index = _random_adjust(
        game.economy.salary_index, min_value=0.8, max_value=1.5, max_pct_change=0.5
    )

    game.economy.tax_rate = _random_adjust(
        game.economy.tax_rate, min_value=1, max_value=5.0, max_pct_change=0.6
    )

    game.economy.inflation = round((game.economy.interest_rate + game.economy.salary_index + game.economy.tax_rate) / 3.0, 2)

def show_graph(game):
    try:
        csv_path = Path(__file__).resolve().parents[1] / "data" / "save" / f"{game.player.name.split()[0]}_economy.csv"
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.read_csv(csv_path.as_posix())
        numeric_cols = df.select_dtypes(include='number').columns

        if 'Day' in numeric_cols:
            plot_cols = [c for c in numeric_cols if c != 'Day']
        else:
            cols = list(df.columns)
            try:
                idx = cols.index('Day')
                plot_cols = cols[idx + 1:]
            except ValueError:
                plot_cols = [c for c in cols if c != 'Day']

        plot_df = df.dropna(subset=plot_cols, how='all')
        fig = plt.figure(figsize=(10,9),dpi=100,facecolor="none",edgecolor='#000')
        fig.suptitle('Economic Indexes',fontsize=30,fontweight='bold')
        plt.xticks(fontsize=20,rotation=30,fontweight='bold')
        plt.yticks(fontsize=20,rotation=30,fontweight='bold')
        plt.ylim(0,10)
        plt.xlabel("Day", fontsize=25,fontweight='bold')
        plt.ylabel("Index", fontsize=25,fontweight='bold')
        sns.set_theme(style='ticks',font='Verdana',font_scale=1)

        sns.lineplot(data=plot_df, x='Day', y=plot_df['Inflation'], label=plot_df['Inflation'].name,linewidth=6,color='blue')
        sns.lineplot(data=plot_df, x='Day', y=plot_df['Interest Rate'], label=plot_df['Interest Rate'].name,linewidth=6,color='lime')
        sns.lineplot(data=plot_df, x='Day', y=plot_df['Salary Index'], label=plot_df['Salary Index'].name,linewidth=6,color='Orange')
        sns.lineplot(data=plot_df, x='Day', y=plot_df['Tax Rate'], label=plot_df['Tax Rate'].name,linewidth=6,color='Red')

        plt.legend(fontsize=25)


        buf = io.BytesIO()
        plt.savefig(buf,format='PNG')
        plt.close(fig)
        buf.seek(0)
        plot_image = pygame.image.load(buf,'plot.png')

        return plot_image
    except FileNotFoundError:
        return None

