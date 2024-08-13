from typing import Iterable, Any, Coroutine, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual import on
from textual.events import Mount, Key, MouseDown
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
from idle_tui_adventures.database.db_transactions import create_new_item
from idle_tui_adventures.database.db_queries import get_all_items


class InventoryEquipScreen(ModalScreen):
    app: "IdleAdventure"
    name: str = "InventoryEquipScreen"
    BINDINGS = [("escape", "app.pop_screen"), ("b", "app.pop_screen")]
    DEFAULT_CSS = """InventoryEquipScreen {
        layout: grid;
        grid-size: 2 2;
        grid-rows: 75% 24%;
        grid-columns: 1fr;
        grid-gutter: 1 4;
        align: center middle;
    }
    """

    def compose(self) -> Iterable[Widget]:
        yield Inventory()
        yield Equipment()
        # yield Placeholder()

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
    def _on_key(self, event: Key) -> Coroutine[Any, Any, None]:
        key_pressed = event.key
        if key_pressed == "space":
            create_new_item(
                name="Axe2 of Ordinary",
                level_needed=1,
                category="Weapon",
                rarity="unique",
                damage=3,
                attack_speed=1.05,
                strength=0,
                intelligence=0,
                dexterity=0,
                luck=2,
                owned_by=1,
            )
            self.notify("Item Created")

        try:
            self.query_one(Inventory).query_one(
                f"#slot_{key_pressed}", Slot
            ).place_item(ItemIcon(item=Item(**get_all_items()[0])))
        except Exception as e:
            self.log.error(e)
        return super()._on_key(event)

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
