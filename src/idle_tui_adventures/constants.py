from typing import Literal, get_args
from pathlib import Path
# from platformdirs import user_data_dir, user_config_dir

# Config related

# Oder ueber die Config dann variabel halten
# CONFIG_PATH = Path(
#     user_config_dir(appname="idle-tui-adventures", appauthor=False, ensure_exists=True)
# )
CONFIG_NAME = "idle_tui_adventures.ini"
CONFIG_PATH = Path(".").cwd()
CONFIG_FULL_PATH = CONFIG_PATH / CONFIG_NAME

# DB related
DB_NAME = "database.db"
DB_PATH = Path(".").cwd()
# DB = Path(
#     user_data_dir(appname="idle-tui-adventures", appauthor=False, ensure_exists=True)
# )
DB_FULL_PATH = DB_PATH / DB_NAME

# Stats related
STATS_LITERAL = Literal["strength", "intelligence", "dexterity", "luck"]
STATS = get_args(STATS_LITERAL)
PROFESSION_MAINSTAT_DICT = {
    "Warrior": "strength",
    "Mage": "intelligence",
    "Ranger": "dexterity",
    "Thief": "luck",
}

# Item-rarity
RARITIES_LITERAL = Literal["common", "rare", "epic", "legendary", "unique"]
RARITIES = get_args(RARITIES_LITERAL)
ITEM_RARITIES_COLOR_DICT = {
    "common": "green",
    "rare": "blue",
    "epic": "red",
    "legendary": "orange",
    "unique": "#aefdfd",
}

# Item-category
ITEM_CATEGORIES_LITERAL = Literal[
    "Consumable",
    "Armor",
    "Helmet",
    "Ring",
    "Weapon",
    "Boots",
    # "Axe",
    # "Scythe",
    # "Shovel",
    # "Wrench",
]
ITEM_CATEGORIES = get_args(ITEM_CATEGORIES_LITERAL)

# Icons-menu
MENU_ICONS_LITERAL = Literal["character", "backpack", "dungeon", "shop", "settings"]
MENU_ICONS = get_args(MENU_ICONS_LITERAL)
ICON_SCREEN_DICT = {
    "character": "CharacterScreen",
    "backpack": "InventoryEquipScreen",
    "dungeon": "DungeonScreen",
    "shop": "ShopScreen",
    "settings": "SettingsScreen",
}

# Icons-professions
PROFESSIONS_LITERAL = Literal["Warrior", "Mage", "Ranger", "Thief"]
PROFESSIONS = get_args(PROFESSIONS_LITERAL)

# Icons-Monster
MONSTERS_LITERAL = Literal["bear", "dragon", "dragon2"]

ICONS_LITERAL = (
    MENU_ICONS_LITERAL
    | PROFESSIONS_LITERAL
    | ITEM_CATEGORIES_LITERAL
    | MONSTERS_LITERAL
)

# Inventory (Row,Cols)
INVENTORY_SIZE = (4, 4)

# Progression
MONSTER_PER_STAGE = 5
