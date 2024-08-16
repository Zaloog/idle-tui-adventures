from typing import Iterable

from textual.widget import Widget
from textual.widgets import Placeholder, Button, Label
from textual.containers import Vertical, Horizontal


class ShopInterface(Vertical):
    def compose(self) -> Iterable[Widget]:
        yield Placeholder("Shop")
        yield Label("Pull Items")
        yield LootBoxRow()
        return super().compose()


class LootBoxRow(Horizontal):
    def compose(self) -> Iterable[Widget]:
        yield Button("Normal\nPull", id="btn_spawn_normal", variant="success")
        yield Button("Epic\nPull", id="btn_spawn_epic", variant="error")
        yield Button("Legend\nPull", id="btn_spawn_legend", variant="warning")
        return super().compose()
