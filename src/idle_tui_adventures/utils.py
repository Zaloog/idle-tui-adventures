from pathlib import Path

from rich_pixels import Pixels

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.widgets.inventory_screen_widgets import Item

from idle_tui_adventures.constants import ITEM_RARITIES_COLOR_DICT


def get_icon(icon: str, width: int = 30, heigth: int = 25) -> Pixels:
    icon_path = Path(__file__).parent / f"./assets/static/image_{icon.lower()}.png"
    return Pixels.from_image_path(icon_path, resize=(width, heigth))


def get_nice_tooltip(item: "Item") -> str | None:
    tooltip_str = (
        f"[{ITEM_RARITIES_COLOR_DICT[item.rarity]}]{item.rarity.capitalize():^20}[/]\n"
    )
    tooltip_str += f"\n[yellow]{item.name}[/]\n\n"
    tooltip_str += f"Level needed: [blue]{item.level_needed:>6}[/]\n"
    tooltip_str += f"Damage: [blue]{item.damage:>12}[/]\n" if item.damage > 0 else ""
    tooltip_str += (
        f"Attack Speed: [blue]{item.attack_speed:>6}[/]\n"
        if item.attack_speed > 0
        else ""
    )
    if sum([item.strength, item.intelligence, item.dexterity, item.luck]) > 0:
        tooltip_str += f"\n[yellow]{'Bonus Stats':-^20}[/]\n\n"
        tooltip_str += (
            f"Strength: [blue]{item.strength:>10}[/]\n" if item.strength > 0 else ""
        )
        tooltip_str += (
            f"Intelligence: [blue]{item.intelligence:>6}[/]\n"
            if item.intelligence > 0
            else ""
        )
        tooltip_str += (
            f"Dexterity: [blue]{item.dexterity:>9}[/]\n" if item.dexterity > 0 else ""
        )
        tooltip_str += f"Luck: [blue]{item.luck:>14}[/]\n" if item.luck > 0 else ""
    return tooltip_str


# exp -> level : (sqrt(100(2experience+25))+50)/100
def calculate_exp_needed(next_lvl: int) -> int:
    return (next_lvl - 1) * next_lvl * 50
