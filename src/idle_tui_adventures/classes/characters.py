from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from idle_tui_adventures.constants import PROFESSIONS_LITERAL
from idle_tui_adventures.classes.items import Item
from idle_tui_adventures.database.db_queries import get_items_for_character
from idle_tui_adventures.database.db_transactions import (
    update_experience_db,
    update_level_db,
    gain_unassigned_stats_db,
    alocate_new_stats_db,
    update_equip_status_item_db,
)


@dataclass
class Character:
    character_id: int
    name: str
    profession: PROFESSIONS_LITERAL
    created_at: datetime
    level: int
    experience: int
    unassigned_stat_points: int
    strength: int
    intelligence: int
    dexterity: int
    luck: int

    def __post_init__(self) -> None:
        # Base Stats
        self.base_damage = 1
        self.base_attack_speed = 1.00
        self.base_crit_rate = 0.05
        self.base_crit_damage_multiplier = 1.20
        # Calculate Stats
        self.equipped_items: list[Item] = []
        self.inventory_items: list[Item] = []
        # self.get_items_from_db()
        self.calculate_stats()

    def level_up(self, database: Path):
        self.level += 1
        update_level_db(
            character_id=self.character_id, level=self.level, database=database
        )
        self.unassigned_stat_points += 5
        gain_unassigned_stats_db(
            character_id=self.character_id, unassigned_stats=5, database=database
        )

    def collect_exp(self, database: Path, exp_amount: int = 1):
        self.experience += exp_amount
        update_experience_db(
            character_id=self.character_id,
            experience=self.experience,
            database=database,
        )

    def update_stats(self, change_stat_dict: dict, database: Path):
        alocate_new_stats_db(
            character_id=self.character_id,
            change_stat_dict=change_stat_dict,
            database=database,
        )
        self.unassigned_stat_points -= sum(change_stat_dict.values())
        for stat, new_value in change_stat_dict.items():
            match stat:
                case "strength":
                    self.strength += new_value
                case "intelligence":
                    self.intelligence += new_value
                case "dexterity":
                    self.dexterity += new_value
                case "luck":
                    self.luck += new_value
        self.calculate_stats()

    def calculate_stats(self) -> None:
        self.damage = self.base_damage + 5 * self.strength
        self.attack_speed = self.base_attack_speed + 0.01 * self.dexterity
        self.crit_rate = self.base_crit_rate + 0.01 * self.luck
        self.crit_damage = self.damage * (
            self.base_crit_damage_multiplier + 0.02 * self.dexterity
        )

    # von db
    def get_items_from_db(self, database: Path) -> None:
        all_items = get_items_for_character(
            character_id=self.character_id, database=database
        )
        self.equipped_items = [Item(**item) for item in all_items if item["equipped"]]
        self.inventory_items = [
            Item(**item) for item in all_items if not item["equipped"]
        ]

    def equip_item(self, item: Item, database: Path):
        update_equip_status_item_db(
            item_id=item.item_id, equipped=True, database=database
        )
        self.get_items_from_db(database=database)
