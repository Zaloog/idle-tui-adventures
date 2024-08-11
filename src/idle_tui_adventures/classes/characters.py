from dataclasses import dataclass
from datetime import datetime

from idle_tui_adventures.constants import PROFESSIONS_LITERAL
from idle_tui_adventures.database.db_transactions import (
    update_experience_db,
    update_level_db,
    gain_unassigned_stats_db,
    alocate_new_stats_db,
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
        self.equipped_items = self.get_equipped_items()
        self.inventory_items = self.get_inventory_items()
        # Calculate Stats
        self.attack_speed = 2.00
        self.crit_rate = 0.40
        self.damage = 100

    def level_up(self):
        self.level += 1
        update_level_db(character_id=self.character_id, level=self.level)
        self.unassigned_stat_points += 5
        gain_unassigned_stats_db(character_id=self.character_id, unassigned_stats=5)

    def collect_exp(self, exp_amount: int = 1):
        self.experience += exp_amount
        update_experience_db(character_id=self.character_id, experience=self.experience)

    def update_stats(self, change_stat_dict: dict):
        alocate_new_stats_db(
            character_id=self.character_id, change_stat_dict=change_stat_dict
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

    # von db
    def get_equipped_items(self): ...
    # von db
    def get_inventory_items(self): ...
