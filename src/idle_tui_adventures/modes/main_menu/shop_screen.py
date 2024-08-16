from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual import on
from textual.events import Mount, MouseDown
from textual.geometry import Offset
from textual.widget import Widget
from textual.screen import ModalScreen
from textual.widgets import Button

from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow, ItemIcon
from idle_tui_adventures.widgets.inventory_screen_widgets import Inventory, Slot
from idle_tui_adventures.widgets.shop_screen_widgets import ShopInterface
from idle_tui_adventures.widgets.modal_floating_screen import ItemPopUpScreen
from idle_tui_adventures.classes.items import Item

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
            pull_variant=rarity,
            owned_by=self.app.character.character_id,
            current_lvl=self.app.character.level,
        )
        self.query_one(Inventory).update_inventory()

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
