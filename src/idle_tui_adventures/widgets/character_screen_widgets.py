from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Placeholder, Label, Button
from textual.containers import Vertical, Horizontal

from idle_tui_adventures.widgets.stat_point_widgets import StatUpdateDisplay


class CharacterInterface(Vertical):
    unassigned_stat_points: reactive[int] = reactive(1)
    spend_stat_points: reactive[int] = reactive(0)

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
        Label {
            text-align: center;
        }

    }

    .-hidden {
        display:none;
    }
    """

    def compose(self) -> Iterable[Widget]:
        yield Placeholder("Character_Infos")
        yield StatUpdateDisplay()
        yield Label("Updates")
        yield ConfirmButtons()
        return super().compose()

    def on_button_pressed(self):
        self.unassigned_stat_points -= 1

    def watch_unassigned_stat_points(self):
        if self.unassigned_stat_points == 0:
            self.query(Button).add_class("-hidden")
        else:
            self.query(Button).remove_class("-hidden")
        self.query_one(Label).update(
            f"available stat points: {self.unassigned_stat_points}"
        )


class ConfirmButtons(Horizontal):
    def compose(self) -> Iterable[Widget]:
        yield Button("Cancel")
        yield Button("Confirm")
        return super().compose()
