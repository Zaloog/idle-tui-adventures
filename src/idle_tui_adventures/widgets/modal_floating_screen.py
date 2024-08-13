from typing import Iterable

from textual import on
from textual.reactive import reactive
from textual.events import MouseUp, MouseMove
from textual.screen import ModalScreen
from textual.widget import Widget

from idle_tui_adventures.widgets.icon_widgets import ItemIcon
from idle_tui_adventures.classes.items import Item
from idle_tui_adventures.widgets.inventory_screen_widgets import EquipSlot, ItemSlot


class ItemPopUpScreen(ModalScreen):
    valid_position: reactive = False

    def __init__(self, clicked_item: Item, slot_list: list[EquipSlot | ItemSlot]):
        self.clicked_item = clicked_item
        self.slot_list = slot_list
        self.initial_position = self.app.mouse_position

        super().__init__()

    def compose(self) -> Iterable[Widget]:
        self.floating_icon = ItemIcon(item=self.clicked_item, relocating=True)
        self.floating_icon.offset = self.app.mouse_position
        yield self.floating_icon
        return super().compose()

    @on(MouseUp)
    def on_mouse_up(self):
        if self.valid_position:
            movement_instructions = (
                self.initial_position,
                self.app.mouse_position,
                self.clicked_item,
            )
        else:
            movement_instructions = None

        self.dismiss(result=movement_instructions)

    @on(MouseMove)
    def on_mouse_move(self):
        self.floating_icon.offset = self.app.mouse_position
        self.valid_position = False
        self.floating_icon.styles.border = "outer", "red"
        self.floating_icon.border_title = ""

        for slot in self.slot_list:
            if slot.region.contains_point(self.app.mouse_position):
                if slot.is_valid(item=self.clicked_item):
                    self.floating_icon.styles.border = "outer", "green"
                    self.floating_icon.border_title = slot.id
                    self.valid_position = True
                else:
                    # self.valid_position = False
                    self.floating_icon.styles.border = "outer", "red"
                    self.floating_icon.border_title = slot.id
