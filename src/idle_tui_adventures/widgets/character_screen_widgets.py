from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual import on
from textual.events import Mount
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Placeholder, Label, Button
from textual.containers import Vertical, Horizontal

from idle_tui_adventures.widgets.stat_point_widgets import (
    StatUpdateDisplay,
    StatChanger,
)


class CharacterInterface(Vertical):
    unassigned_stat_points: reactive[int] = reactive(0)
    spent_stat_points: reactive[int] = reactive(0)
    spent_stat_dict: reactive[dict] = reactive(
        {
            "strength": 0,
            "intelligence": 0,
            "dexterity": 0,
            "luck": 0,
        }
    )

    app: "IdleAdventure"
    DEFAULT_CSS = """
    CharacterInterface {
        width: 1fr;
        height: 1fr;
        align:center middle;

        Placeholder {
            height: 15%;
        }
        StatUpdateDisplay {
            height: 70%;
        }
        Label {
            width:1fr;
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
        yield Label("no points to spend")
        yield ConfirmButtons()
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.app.character.unassigned_stat_points = 3
        self.unassigned_stat_points = self.app.character.unassigned_stat_points

        return super()._on_mount(event)

    def watch_spent_stat_points(self):
        self.query_one(Label).update(
            f"points to spend: {self.unassigned_stat_points - self.spent_stat_points}"
        )

    @on(StatChanger.SpentPoint)
    def spent_point(self, event: StatChanger.SpentPoint):
        self.spent_stat_points += 1
        self.spent_stat_dict[event.statchanger.stat] += 1
        self.mutate_reactive(CharacterInterface.spent_stat_dict)

    @on(StatChanger.UnspentPoint)
    def unspent_point(self, event: StatChanger.SpentPoint):
        self.spent_stat_points -= 1
        self.spent_stat_dict[event.statchanger.stat] -= 1
        self.mutate_reactive(CharacterInterface.spent_stat_dict)

    def watch_spent_stat_dict(self):
        self.log.error(self.spent_stat_dict)
        self.log.error(sum(self.spent_stat_dict.values()))

        if sum(self.spent_stat_dict.values()) == self.unassigned_stat_points:
            self.query(Button).filter(".assign_point").set_styles("visibility: hidden;")
        else:
            self.query(Button).filter(".assign_point").set_styles(
                "visibility: visible;"
            )

        for stat, spent_points in self.spent_stat_dict.items():
            if spent_points == 0:
                self.query_one(f"#btn_decrease_{stat}", Button).set_styles(
                    "visibility: hidden;"
                )
            else:
                self.query_one(f"#btn_decrease_{stat}", Button).set_styles(
                    "visibility: visible;"
                )

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
    DEFAULT_CSS = """
    ConfirmButtons {
        width: 1fr;
        height: auto;
        dock:bottom;
        Button {
            width:1fr;
        }
    }
    """

    def compose(self) -> Iterable[Widget]:
        yield Button("Cancel", id="revert_stats", variant="error")
        yield Button("Confirm", id="confirm_stats", variant="success")
        return super().compose()
