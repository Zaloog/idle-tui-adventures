from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual import on
from textual.events import Mount
from textual.widget import Widget
from textual.screen import ModalScreen
from textual.widgets import Button

from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow
from idle_tui_adventures.widgets.inventory_screen_widgets import Inventory
from idle_tui_adventures.widgets.shop_screen_widgets import ShopInterface

from idle_tui_adventures.odds import create_new_equipment


class ShopScreen(ModalScreen):
    app: "IdleAdventure"
    name: str = "ShopScreen"
    BINDINGS = [("escape", "app.pop_screen"), ("l", "app.pop_screen")]

    def compose(self) -> Iterable[Widget]:
        yield Inventory()
        yield ShopInterface()
        yield MenuIconsRow()
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.query_one("#shop").add_class("-active")
        return super()._on_mount(event)

    @on(Button.Pressed)
    def pull_item(self, event: Button.Pressed):
        rarity = event.button.id.split("_")[-1]
        self.notify(message=rarity)
        create_new_equipment(
            owned_by=self.app.character.character_id,
            current_lvl=self.app.character.level,
        )
        self.query_one(Inventory).update_inventory()
