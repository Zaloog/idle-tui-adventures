import sqlite3
from datetime import datetime
from pathlib import Path

from idle_tui_adventures.database.db_utils import create_connection
from idle_tui_adventures.constants import (
    PROFESSIONS_LITERAL,
    DB_FULL_PATH,
    RARITIES_LITERAL,
    ITEM_CATEGORIES_LITERAL,
)


def create_new_character_db(
    name: str,
    profession: PROFESSIONS_LITERAL,
    strength: int,
    intelligence: int,
    dexterity: int,
    luck: int,
    database: Path = DB_FULL_PATH,
) -> str | int:
    data_character_dict = {
        "name": name,
        "profession": profession,
        "strength": strength,
        "intelligence": intelligence,
        "dexterity": dexterity,
        "luck": luck,
        "unassigned_stat_points": 0,
        "creation_time": datetime.now().replace(microsecond=0),
        "level": 1,
        "experience": 0,
    }

    transaction_str = """
    INSERT INTO characters
    VALUES (
        NULL,
        :name,
        :profession,
        :creation_time,
        :level,
        :experience,
        :unassigned_stat_points,
        :strength,
        :intelligence,
        :dexterity,
        :luck
        );"""

    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, data_character_dict)
            con.commit()
            return 0
        except sqlite3.Error as e:
            con.rollback()
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_CHECK:
                return "please provide a character name"
            elif e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                return "character name already taken"
            return e.sqlite_errorname


def create_new_item_db(
    name: str,
    level_needed: int,
    rarity: RARITIES_LITERAL,
    category: ITEM_CATEGORIES_LITERAL,
    damage: int,
    attack_speed: float,
    strength: int,
    intelligence: int,
    dexterity: int,
    luck: int,
    owned_by: int,
    database: Path = DB_FULL_PATH,
) -> str | int:
    data_item_dict = {
        "name": name,
        "rarity": rarity,
        "category": category,
        "level_needed": level_needed,
        "damage": damage,
        "attack_speed": attack_speed,
        "strength": strength,
        "intelligence": intelligence,
        "dexterity": dexterity,
        "luck": luck,
        "owned_by": owned_by,
        "equipped": False,
    }

    transaction_str = """
    INSERT INTO items
    VALUES (
        NULL,
        :name,
        :rarity,
        :category,
        :level_needed,
        :damage,
        :attack_speed,
        :strength,
        :intelligence,
        :dexterity,
        :luck,
        :owned_by,
        :equipped
        );"""

    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, data_item_dict)
            con.commit()
            return 0
        except sqlite3.Error as e:
            con.rollback()
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_CHECK:
                return "Item Insertion Error"
            elif e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                return "Iterm Insertion Error"
            return e.sqlite_errorname


def update_experience_db(
    character_id: int, experience: int, database: Path = DB_FULL_PATH
) -> int | str:
    exp_dict = {"character_id": character_id, "experience": experience}
    transaction_str = """
    UPDATE characters
    SET experience = :experience
    WHERE character_id = :character_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, exp_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname


def update_level_db(
    character_id: int, level: int, database: Path = DB_FULL_PATH
) -> int | str:
    lvl_dict = {"character_id": character_id, "level": level}
    transaction_str = """
    UPDATE characters
    SET level = :level
    WHERE character_id = :character_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, lvl_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname


def gain_unassigned_stats_db(
    character_id: int, unassigned_stats: int, database: Path = DB_FULL_PATH
) -> int | str:
    gain_stat_dict = {
        "character_id": character_id,
        "unassigned_stat_points": unassigned_stats,
    }
    transaction_str = """
    UPDATE characters
    SET unassigned_stat_points = unassigned_stat_points + :unassigned_stat_points
    WHERE character_id = :character_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, gain_stat_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname


def alocate_new_stats_db(
    character_id: int, change_stat_dict: dict, database: Path = DB_FULL_PATH
) -> int | str:
    used_stat_points = sum(change_stat_dict.values())
    alocate_stat_dict = {
        "character_id": character_id,
        "used_points": used_stat_points,
    } | change_stat_dict
    transaction_str = """
    UPDATE characters
    SET
        strength = strength + :strength,
        intelligence = intelligence + :intelligence,
        dexterity = dexterity + :dexterity,
        luck = luck + :luck,
        unassigned_stat_points = unassigned_stat_points - :used_points
    WHERE character_id = :character_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, alocate_stat_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname


def update_monsters_killed_db(
    gamestate_id: int, database: Path = DB_FULL_PATH
) -> int | str:
    gamestate_dict = {
        "gamestate_id": gamestate_id,
    }
    transaction_str = """
    UPDATE gamestates
    SET monsters_killed = monsters_killed + 1
    WHERE gamestate_id = :gamestate_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, gamestate_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname


def update_major_stage_db(
    gamestate_id: int, major_stage: int, database: Path = DB_FULL_PATH
) -> int | str:
    gamestate_dict = {"gamestate_id": gamestate_id, "major_stage": major_stage}
    transaction_str = """
    UPDATE gamestates
    SET major_stage = :major_stage
    WHERE gamestate_id = :gamestate_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, gamestate_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname


def update_minor_stage_db(
    gamestate_id: int, minor_stage: int, database: Path = DB_FULL_PATH
) -> int | str:
    gamestate_dict = {"gamestate_id": gamestate_id, "minor_stage": minor_stage}
    transaction_str = """
    UPDATE gamestates
    SET minor_stage = :minor_stage
    WHERE gamestate_id = :gamestate_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, gamestate_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname


def create_initial_gamestate(character_id: int, database: Path = DB_FULL_PATH):
    gamestate_dict = {
        "character_playing": character_id,
        "major_stage": 1,
        "minor_stage": 1,
        "monsters_killed": 0,
    }

    transaction_str = """
    INSERT INTO gamestates
    VALUES (
        NULL,
        :character_playing,
        :major_stage,
        :minor_stage,
        :monsters_killed
        )
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, gamestate_dict)
            con.commit()
            return 0
        except sqlite3.Error as e:
            con.rollback()
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_CHECK:
                return "Item Insertion Error"
            elif e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                return "Iterm Insertion Error"
            return e.sqlite_errorname


def update_equip_status_item_db(
    item_id: int, equipped: bool, database: Path = DB_FULL_PATH
) -> int | str:
    equip_dict = {"item_id": item_id, "equipped": equipped}
    transaction_str = """
    UPDATE items
    SET equipped = :equipped
    WHERE item_id = :item_id
    """
    with create_connection(database=database) as con:
        con.row_factory = sqlite3.Row
        try:
            con.execute(transaction_str, equip_dict)
            return 0
        except sqlite3.Error as e:
            print(e.sqlite_errorname)
            return e.sqlite_errorname
