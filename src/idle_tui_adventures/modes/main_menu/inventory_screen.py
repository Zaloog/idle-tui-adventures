from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual import on
from textual.events import Mount, MouseDown
from textual.geometry import Offset
from textual.widget import Widget
from textual.screen import ModalScreen

from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow, ItemIcon
from idle_tui_adventures.widgets.inventory_screen_widgets import (
    Inventory,
    Equipment,
    Slot,
)
from idle_tui_adventures.classes.items import Item
from idle_tui_adventures.widgets.modal_floating_screen import ItemPopUpScreen


class InventoryEquipScreen(ModalScreen):
    app: "IdleAdventure"
    name: str = "InventoryEquipScreen"
    BINDINGS = [("escape", "app.pop_screen"), ("b", "app.pop_screen")]

    def compose(self) -> Iterable[Widget]:
        yield Inventory()
        yield Equipment()

        yield MenuIconsRow()
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.query_one("#backpack").add_class("-active")
        for i, item in enumerate(self.app.character.inventory_items):
            self.query_one(Inventory).query_one(f"#slot_{i}", Slot).place_item(
                ItemIcon(item=item)
            )

        return super()._on_mount(event)

    # Temporary

    @on(MouseDown)
    def select_new_item_position(self, event: MouseDown):
        if event.button == 1:
            item_icon_to_move, _ = self.get_widget_at(*event.screen_offset)
            if isinstance(item_icon_to_move, ItemIcon):
                slot_list = [slot for slot in self.query(Slot)]
                self.app.push_screen(
                    ItemPopUpScreen(
                        clicked_item=item_icon_to_move.item, slot_list=slot_list
                    ),
                    callback=self.relocate_item,
                )

    def relocate_item(self, movement_instructions: tuple[Offset, Offset, Item] | None):
        if movement_instructions is not None:
            initial_slot_widget: Slot = list(
                self.get_widgets_at(*movement_instructions[0])
            )[1][0]
            target_slot_widget: Slot = self.get_widget_at(*movement_instructions[1])[0]
            target_item = movement_instructions[2]

            initial_slot_widget.remove_item()
            target_slot_widget.place_item(item=ItemIcon(target_item))
