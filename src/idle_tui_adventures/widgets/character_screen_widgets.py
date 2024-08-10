from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual.events import Mount
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Placeholder, Label, Button
from textual.containers import Vertical, Horizontal

from idle_tui_adventures.widgets.stat_point_widgets import (
    StatUpdateDisplay,
)


class CharacterInterface(Vertical):
    unassigned_stat_points: reactive[int] = reactive(0)
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

    """

    def __init__(self) -> None:
        self.current_stat_dict = {
            "strength": self.app.character.strength,
            "intelligence": self.app.character.intelligence,
            "dexterity": self.app.character.dexterity,
            "luck": self.app.character.luck,
        }
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield Placeholder("Character_Infos")
        yield StatUpdateDisplay(current_stat_dict=self.current_stat_dict)
        yield Label("Updates")
        yield ConfirmButtons()
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.app.character.unassigned_stat_points = 3
        self.unassigned_stat_points = self.app.character.unassigned_stat_points

        return super()._on_mount(event)

    # def on_button_pressed(self, event: Button.Pressed):
    #     if "assign_point" in event.button.classes:
    #         self.spend_stat_points += 1
    #         self.query_one(
    #             f'#stat_{event.button.id.split("_")[-1]}', StatDisplayWithoutButton
    #         ).increase_value(1)
    #     if "undo_assign" in event.button.classes:
    #         self.spend_stat_points -= 1
    #         self.query_one(
    #             f'#stat_{event.button.id.split("_")[-1]}', StatDisplayWithoutButton
    #         ).decrease_value(1)
    #     self.log.error(
    #         f"unassigned {self.unassigned_stat_points}, spend {self.spend_stat_points}"
    #     )

    # def watch_spend_stat_points(self):
    #     if self.spend_stat_points == 0:
    #         self.query(Button).filter(".undo_assign").set_styles("visibility: hidden;")
    #     else:
    #         self.query(Button).filter(".undo_assign").set_styles("visibility: visible;")

    #     if self.spend_stat_points == self.unassigned_stat_points:
    #         self.query(Button).filter(".assign_point").set_styles("visibility: hidden;")
    #     else:
    #         self.query(Button).filter(".assign_point").set_styles(
    #             "visibility: visible;"
    #         )
    #     self.query_one(Label).update(
    #         f"available stat points: {self.unassigned_stat_points - self.spend_stat_points}"
    #     )


class ConfirmButtons(Horizontal):
    def compose(self) -> Iterable[Widget]:
        yield Button("Cancel", id="revert_stats")
        yield Button("Confirm", id="confirm_stats")
        return super().compose()
