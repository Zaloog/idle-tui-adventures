from typing import Iterable

from textual.events import Mount
from textual.widget import Widget
from textual.screen import ModalScreen

from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow
from idle_tui_adventures.widgets.inventory_screen_widgets import Inventory
from idle_tui_adventures.widgets.shop_screen_widgets import ShopInterface


class ShopScreen(ModalScreen):
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
