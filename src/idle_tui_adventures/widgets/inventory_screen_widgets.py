from math import prod
from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual.events import Mount
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Grid

from idle_tui_adventures.constants import INVENTORY_SIZE, ITEM_CATEGORIES_LITERAL
from idle_tui_adventures.classes.items import Item
from idle_tui_adventures.widgets.icon_widgets import ItemIcon


class Inventory(Grid):
    app: "IdleAdventure"
    inventory_dict: dict

    DEFAULT_CSS = (
        """
    Inventory {
        grid-size: %d %d;

        ItemSlot {
            width:1fr;
            height:1fr;
        }
    }
    """
        % INVENTORY_SIZE
    )

    def compose(self) -> Iterable[Widget]:
        for i in range(prod(INVENTORY_SIZE)):
            yield ItemSlot(id=f"slot_{i}")

        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.fill_inventory()
        return super()._on_mount(event)

    def fill_inventory(self):
        for i, item in enumerate(self.app.character.inventory_items):
            self.query_one(f"#slot_{i}", Slot).place_item(ItemIcon(item=item))

    def update_inventory(self):
        self.recompose()
        self.app.character.get_items_from_db(database=self.app.cfg.database_path)
        for i, item in enumerate(self.app.character.inventory_items):
            self.query_one(f"#slot_{i}", Slot).place_item(ItemIcon(item=item))


class Equipment(Grid):
    equipment_dict: dict

    # On Mount?
    # Change Layout
    # query items
    # place items

    def compose(self) -> Iterable[Widget]:
        yield EquipSlot(id="slot_helmet", category="Helmet")
        yield EquipSlot(id="slot_armor", category="Armor")
        yield EquipSlot(id="slot_boots", category="Boots")
        yield EquipSlot(id="slot_weapon1", category="Weapon")
        yield EquipSlot(id="slot_weapon2", category="Weapon")
        yield EquipSlot(id="slot_ring1", category="Ring")
        yield EquipSlot(id="slot_ring2", category="Ring")

        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        for slot in self.query(EquipSlot):
            slot.update(slot.category)
        return super()._on_mount(event)


class Slot(Static):
    amount: reactive = reactive(0)
    empty: reactive = reactive(True)

    def __init__(self, id: str | None = None) -> None:
        super().__init__(id=id)

    def compose(self) -> Iterable[Widget]:
        self.styles.border_subtitle_color = "yellow"
        self.border_subtitle = f"{self.amount} x" if self.amount else ""
        return super().compose()

    def place_item(self, item: Item) -> None:
        if self.empty:
            self.mount(item)
            self.amount = 1
            self.empty = False

    def remove_item(self) -> None:
        if not self.empty:
            self.query_one(ItemIcon).remove()
            self.amount -= 1
            self.empty = True

    def watch_amount(self):
        self.border_subtitle = f"{self.amount} x" if self.amount else ""


class ItemSlot(Slot):
    DEFAULT_CSS = """ItemSlot {
        width: 1fr;
        height: 1fr;
        align: center middle;
        content-align: center middle;
        background: #ba9f68;
        border:outer #6a4f32;
        border-subtitle-background:#6a4f32;

    }"""

    def __init__(self, id: str | None = None) -> None:
        super().__init__(id)

    def is_valid(self, item: Item) -> bool:
        # item stackable?
        if not self.empty:
            return False
        return True


class EquipSlot(Slot):
    empty: bool = True

    DEFAULT_CSS = """EquipSlot {
        width: 1fr;
        height: 1fr;
        align: center middle;
        content-align: center middle;
        background:  #6b6c6f;
        border:outer #474748;
        border-subtitle-background:#474748;

    }"""

    def __init__(
        self,
        category: ITEM_CATEGORIES_LITERAL,
        id: str | None = None,
    ) -> None:
        self.category = category
        super().__init__(id)

    def is_valid(self, item: Item) -> bool:
        if self.category != item.category:
            return False
        if not self.empty:
            return False
        return True
