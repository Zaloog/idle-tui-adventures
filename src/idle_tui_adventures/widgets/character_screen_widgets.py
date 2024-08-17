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
    StatDisplayWithChange,
    StatChanger,
)


class CharacterInterface(Vertical):
    unassigned_stat_points: reactive[int] = reactive(0, init=False, always_update=True)
    spent_stat_points: reactive[int] = reactive(
        0,
    )
    spent_stat_dict: reactive[dict] = reactive(
        {
            "strength": 0,
            "intelligence": 0,
            "dexterity": 0,
            "luck": 0,
        },
        always_update=True,
    )

    app: "IdleAdventure"

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
        self.unassigned_stat_points = self.app.character.unassigned_stat_points

        return super()._on_mount(event)

    def watch_unassigned_stat_points(self):
        self.query_one(Label).update(
            f"points to spend: {self.unassigned_stat_points - self.spent_stat_points}"
        )
        if self.unassigned_stat_points > 0:
            self.query(Button).exclude(
                ".unassign_point,#confirm_stats,#revert_stats"
            ).set_styles("visibility: visible;")
        else:
            self.query(Button).set_styles("visibility: hidden;")

    def watch_spent_stat_points(self):
        self.query_one(Label).update(
            f"points to spend: {self.unassigned_stat_points - self.spent_stat_points}"
        )
        if self.spent_stat_points > 0:
            self.query(Button).filter("#confirm_stats,#revert_stats").set_styles(
                "visibility: visible;"
            )
        else:
            self.query(Button).filter("#confirm_stats,#revert_stats").set_styles(
                "visibility: hidden;"
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

    @on(Button.Pressed, "#confirm_stats")
    def confirm_stat_selection(self):
        for stat in self.current_stat_dict:
            self.current_stat_dict[stat] += self.spent_stat_dict[stat]
            self.query_one(
                f"#stat_display_{stat}", StatDisplayWithChange
            ).change_value = 0
            self.query_one(
                f"#stat_display_{stat}", StatDisplayWithChange
            ).added_value += self.spent_stat_dict[stat]

        self.unassigned_stat_points -= self.spent_stat_points
        self.spent_stat_points = 0
        self.app.character.update_stats(
            change_stat_dict=self.spent_stat_dict, database=self.app.cfg.database_path
        )
        self.spent_stat_dict = {stat: 0 for stat in self.spent_stat_dict}
        self.mutate_reactive(CharacterInterface.spent_stat_dict)

    @on(Button.Pressed, "#revert_stats")
    def revert_stat_selection(self):
        self.spent_stat_dict = {stat: 0 for stat in self.spent_stat_dict}
        self.spent_stat_points = 0
        for stat_display in self.query(StatDisplayWithChange):
            stat_display.change_value = 0
        self.mutate_reactive(CharacterInterface.spent_stat_dict)


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
