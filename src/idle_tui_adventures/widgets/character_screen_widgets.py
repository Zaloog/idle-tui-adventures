from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual.widget import Widget
from textual.widgets import Placeholder, Label, Button
from textual.containers import Vertical

from idle_tui_adventures.widgets.stat_point_widgets import StatUpdateDisplay


class CharacterInterface(Vertical):
    app: "IdleAdventure"
    DEFAULT_CSS = """
    CharacterInterface {
        width: 1fr;
        height: 1fr;

        Placeholder {
            height: 15%;
        }
        StatUpdateDisplay {
            height: 70%;
        }
    }
    """

    def compose(self) -> Iterable[Widget]:
        yield Placeholder("Character_Infos")
        yield StatUpdateDisplay()
        yield Label("Updates")
        yield Button("Updates")
        return super().compose()
