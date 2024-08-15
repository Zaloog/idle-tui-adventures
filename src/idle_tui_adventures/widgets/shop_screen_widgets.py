from typing import Iterable

from textual.widget import Widget
from textual.widgets import Placeholder
from textual.containers import Vertical


class ShopInterface(Vertical):
    def compose(self) -> Iterable[Widget]:
        yield Placeholder("Shop")
        return super().compose()
