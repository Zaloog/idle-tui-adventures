import sqlite3
from pathlib import Path

from idle_tui_adventures.constants import (
    DB_FULL_PATH,
)


def create_connection(database: Path = DB_FULL_PATH) -> sqlite3.Connection:
    return sqlite3.connect(database=database)


def init_new_db(database: Path = DB_FULL_PATH):
    if database.exists():
        return

    char_db_creation_str = """
    CREATE TABLE IF NOT EXISTS characters (
    character_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    profession TEXT NOT NULL,
    created_at TIMESTAMP,
    level INTEGER NOT NULL,
    experience INTEGER NOT NULL,
    unassigned_stat_points INTEGER NOT NULL,
    strength INTEGER NOT NULL,
    intelligence INTEGER NOT NULL,
    dexterity INTEGER NOT NULL,
    luck INTEGER NOT NULL,
    CHECK (name <> ""),
    CHECK (profession in ('Mage', 'Warrior', 'Ranger', 'Thief'))
    );
    """

    item_db_creation_str = """
    CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rarity TEXT NOT NULL,
    category TEXT NOT NULL,
    level_needed INTEGER NOT NULL,
    damage INTEGER NOT NULL,
    attack_speed REAL NOT NULL,
    strength INTEGER NOT NULL,
    intelligence INTEGER NOT NULL,
    dexterity INTEGER NOT NULL,
    luck INTEGER NOT NULL,
    owned_by INTEGER NOT NULL,
    equipped BOOLEAN,
    FOREIGN KEY (owned_by) REFERENCES characters(character_id)
    );
    """

    gamestate_db_creation_str = """
    CREATE TABLE IF NOT EXISTS gamestates (
    gamestate_id INTEGER PRIMARY KEY,
    character_playing INTEGER NOT NULL,
    major_stage INTEGER NOT NULL,
    minor_stage INTEGER NOT NULL,
    monsters_killed INTEGER NOT NULL,
    FOREIGN KEY (character_playing) REFERENCES characters(character_id)
    );
    """

    indexes_creation_str = """
    CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name);
    CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);
    CREATE INDEX IF NOT EXISTS idx_gamestate_id ON gamestates(gamestate_id);
    """

    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(char_db_creation_str)
            con.execute(item_db_creation_str)
            con.execute(gamestate_db_creation_str)
            con.executescript(indexes_creation_str)

            return 0
        except sqlite3.Error as e:
            print(e)
            con.rollback()
            return 1
