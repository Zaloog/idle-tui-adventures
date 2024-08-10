import sqlite3
from pathlib import Path

from idle_tui_adventures.database.db_utils import create_connection
from idle_tui_adventures.constants import DB_FULL_PATH


def get_all_characters(database: Path = DB_FULL_PATH) -> list[sqlite3.Row]:
    query_str = """
    SELECT *
    FROM characters
    """
    characters = []
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            for row in con.execute(query_str).fetchall():
                characters.append(row)
            return characters
        except sqlite3.Error as e:
            print(e)
            return characters


def get_character_by_id(
    character_id: int, database: Path = DB_FULL_PATH
) -> sqlite3.Row | None:
    query_str = """
    SELECT *
    FROM characters
    WHERE character_id = ?
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            character = con.execute(query_str, (character_id,)).fetchone()
            return character
        except sqlite3.Error as e:
            print(e)
            return None


def get_stages_for_character(
    character_id: int, database: Path = DB_FULL_PATH
) -> sqlite3.Row | None:
    query_str = """
    SELECT major_stage, minor_stage
    FROM gamestates
    WHERE character_playing = ?
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            gamestate = con.execute(query_str, (character_id,)).fetchone()
            return gamestate
        except sqlite3.Error as e:
            print(e)
            return None


def get_gamestate_for_character(
    character_id: int, database: Path = DB_FULL_PATH
) -> sqlite3.Row | None:
    query_str = """
    SELECT *
    FROM gamestates
    WHERE character_playing = ?
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            gamestate = con.execute(query_str, (character_id,)).fetchone()
            return gamestate
        except sqlite3.Error as e:
            print(e)
            return None


def get_all_items(database: Path = DB_FULL_PATH) -> list[sqlite3.Row]:
    query_str = """
    SELECT *
    FROM items
    """

    items = []
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            for row in con.execute(query_str).fetchall():
                items.append(row)
            return items
        except sqlite3.Error as e:
            print(e)
            return items
