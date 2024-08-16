import random
from typing import Literal, get_args, Any
from collections import Counter

from idle_tui_adventures.database.db_transactions import create_new_item_db
from idle_tui_adventures.constants import (
    PROFESSIONS_LITERAL,
    STATS,
    RARITIES,
    RARITIES_LITERAL,
)


MIN_START_STAT = 18
MAX_START_STAT = 22
START_STAT_DISTRIBUTION_DICT = {
    "Warrior": [0.4, 0.2, 0.2, 0.2],
    "Mage": [0.2, 0.4, 0.2, 0.2],
    "Ranger": [0.2, 0.2, 0.4, 0.2],
    "Thief": [0.2, 0.2, 0.2, 0.4],
}


# Random Stuff for Item and Character Creation


def get_random_amount_start_stats(profession: PROFESSIONS_LITERAL):
    amount_stats = random.randint(MIN_START_STAT, MAX_START_STAT)
    return Counter(
        random.choices(
            population=STATS,
            weights=START_STAT_DISTRIBUTION_DICT[profession],
            k=amount_stats,
        )
    )


NAME_EQUIPMENT_OPTIONS_LITERAL = Literal[
    "Armor",
    "Helmet",
    "Ring",
    "Axe",
    "Scythe",
    "Shovel",
    "Wrench",
]
NAME_EQUIPMENT_OPTIONS = get_args(NAME_EQUIPMENT_OPTIONS_LITERAL)

ADJ_EQUIPMENT_OPTIONS_LITERAL = Literal[
    "Strength",
    "Intelligence",
    "Dexterity",
    "Luck",
    "Fury",  # str + int
    "Marksmanship",  # str + dex
    "Rage",  # str + luk
    "Wisdom",  # int + dex
    "Gamble",  # int + luk
    "Bane",  # dex + luk
]
ADJ_EQUIPMENT_OPTIONS = get_args(ADJ_EQUIPMENT_OPTIONS_LITERAL)

LEVEL_DROP_SPAN = 2

RARITIES_DROP_CANCE = [
    0.54,
    0.30,
    0.10,
    0.05,
    0.01,
]


def get_random_equipment_name() -> tuple[Any, Any]:
    equip_category = random.choice(NAME_EQUIPMENT_OPTIONS)
    equip_adjective = random.choice(ADJ_EQUIPMENT_OPTIONS)

    return equip_category, equip_adjective


def get_random_level_needed(current_lvl: int) -> int:
    return max(
        1, random.randint(current_lvl - LEVEL_DROP_SPAN, current_lvl + LEVEL_DROP_SPAN)
    )


# add multiplier
def get_random_rarity() -> RARITIES_LITERAL:
    return random.choices(population=RARITIES, weights=RARITIES_DROP_CANCE, k=1)[0]


DAMAGE_SPAN = 0.1  # +-10%
DMG_PER_LV = 20


def get_random_base_damage(weapon_lvl: int) -> int:
    return random.randint(
        int(weapon_lvl * DMG_PER_LV * (1 - DAMAGE_SPAN)),
        int(weapon_lvl * DMG_PER_LV * (1 + DAMAGE_SPAN)),
    )


def create_new_equipment(owned_by: int, current_lvl: int) -> None:
    category, adjective = get_random_equipment_name()
    level_needed = get_random_level_needed(current_lvl=current_lvl)

    create_new_item_db(
        name=f"{category} of {adjective}",
        level_needed=level_needed,
        rarity=get_random_rarity(),
        category=category,
        damage=get_random_base_damage(weapon_lvl=level_needed),
        attack_speed=1.00,
        strength=0,
        intelligence=0,
        dexterity=0,
        luck=0,
        owned_by=owned_by,
    )
