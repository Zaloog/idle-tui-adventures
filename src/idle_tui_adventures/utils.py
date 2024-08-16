from pathlib import Path

from rich_pixels import Pixels

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.widgets.inventory_screen_widgets import Item

from idle_tui_adventures.constants import (
    ICONS_LITERAL,
)


def get_icon(icon: ICONS_LITERAL, width: int = 30, heigth: int = 25) -> Pixels:
    icon_path = Path(__file__).parent / f"./assets/static/image_{icon.lower()}.png"
    return Pixels.from_image_path(icon_path, resize=(width, heigth))


def get_nice_tooltip(item: "Item") -> str | None:
    return item.__repr__()


# exp -> level : (sqrt(100(2experience+25))+50)/100
def calculate_exp_needed(next_lvl: int) -> int:
    return (next_lvl - 1) * next_lvl * 50
