from __future__ import annotations

from typing import Iterable

from textual import on
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Digits, Button
from textual.containers import Horizontal, Vertical

from idle_tui_adventures.constants import STATS_LITERAL, STATS, PROFESSION_MAINSTAT_DICT
from idle_tui_adventures.utils import get_random_amount_start_stats


class StartStatRandomizer(Vertical):
    def compose(self) -> Iterable[Widget]:
        for stat in STATS:
            yield StatDisplayWithoutButton(stat=stat, value=0)
        yield Button("Randomize", id="btn_randomize")
        return super().compose()

    def get_stat_dict(self):
        return {
            stat: self.query_one(f"#stat_{stat}", StatDisplayWithoutButton).int_value
            for stat in STATS
        }

    @on(Button.Pressed, "#btn_randomize")
    def reroll_stats(self):
        random_stat_dict = get_random_amount_start_stats(
            profession=self.parent.parent.query_one("#select_profession_choice").value
        )
        for stat in STATS:
            self.query_one(f"#stat_{stat}", StatDisplayWithoutButton).set_value(
                random_stat_dict[stat]
            )

    @property
    def stat_int(self) -> StatDisplayWithoutButton:
        return self.query_one("#stat_intelligence")

    @property
    def stat_str(self) -> StatDisplayWithoutButton:
        return self.query_one("#stat_strenght")

    @property
    def stat_dex(self) -> StatDisplayWithoutButton:
        return self.query_one("#stat_dexterity")

    @property
    def stat_luc(self) -> StatDisplayWithoutButton:
        return self.query_one("#stat_luck")


class StatDisplayWithoutButton(Digits):
    DEFAULT_CSS = """ StatDisplayWithoutButton {
        border: solid brown;
        width:1fr;
        height:1fr;
        content-align:center middle;
        text-align:center;

    }
    """

    def __init__(self, stat: STATS_LITERAL, value: int):
        self.stat = stat
        super().__init__(value=f"{value}", id=f"stat_{stat}")

    def compose(self) -> Iterable[Widget]:
        self.border_title = self.stat
        self.styles.border_title_color = "red"

        return super().compose()

    def set_value(self, int_val):
        self.update(value=str(int_val))

    def increase_value(self, increase):
        self.update(value=f"{self.int_value+increase}")

    def decrease_value(self, decrease):
        self.update(value=f"{self.int_value - decrease}")

    @property
    def int_value(self) -> int:
        return int(self.value)

    def highlight_main_stat(self):
        self.border_subtitle = "Main Attribute"
        self.styles.border_subtitle_color = "yellow"

    def reset_highlight(self):
        self.border_subtitle = None
        self.styles.border_subtitle_color = None


class StatUpdateDisplay(Vertical):
    DEFAULT_CSS = """
    StatDisplay {
        layout:grid;
        grid-size: 1 4;
        grid-rows: 1fr;
        width: 1fr;
        align: center middle;
    }
    """

    def __init__(self, current_stat_dict) -> None:  #: dict[STATS_LITERAL, int]
        self.current_stat_dict = current_stat_dict
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        for stat, value in self.current_stat_dict.items():
            yield StatChanger(stat=stat, current_value=value)
        return super().compose()


class StatChanger(Horizontal):
    DEFAULT_CSS = """
    StatDisplayWithButton {
        layout: grid;
        grid-size: 3 1;
        grid-gutter:0 2;
        grid-columns: 1fr 2fr 1fr;
        height:1fr;
        align: center middle;
        content-align: center middle;

        Button {
            height: 1fr;
            width: 1fr;
            margin:1 1 1 1;
        }


    }
    """

    class SpentPoint(Message):
        def __init__(self, statchanger: StatChanger):
            self.statchanger = statchanger
            super().__init__()

        @property
        def control(self) -> StatChanger:
            return self.statchanger

    class UnspentPoint(Message):
        def __init__(self, statchanger: StatChanger):
            self.statchanger = statchanger
            super().__init__()

        @property
        def control(self) -> StatChanger:
            return self.statchanger

    def __init__(self, stat: STATS_LITERAL, current_value: int):
        self.stat = stat
        self.value = current_value
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield Button(
            "-",
            variant="primary",
            classes="unassign_point",
            id=f"btn_decrease_{self.stat}",
        )
        yield StatDisplayWithChange(stat=self.stat, value=self.value)
        yield Button(
            "+",
            variant="primary",
            classes="assign_point",
            id=f"btn_increase_{self.stat}",
        )
        return super().compose()

    def on_button_pressed(self, event: Button.Pressed):
        if "increase" in event.button.id:
            self.query_one(StatDisplayWithChange).change_value += 1
            self.post_message(self.SpentPoint(self))
        if ("decrease" in event.button.id) and (
            self.query_one(StatDisplayWithChange).change_value > 0
        ):
            self.query_one(StatDisplayWithChange).change_value -= 1
            self.post_message(self.UnspentPoint(self))


class StatDisplayWithChange(Horizontal):
    change_value: reactive[int] = reactive(0, init=False)
    added_value: reactive[int] = reactive(0, init=False)

    DEFAULT_CSS = """ StatDisplayWithChange {
        border: solid brown;
        width:1fr;
        height:auto;
        content-align:center middle;

        & Digits {
            text-align:center;
            content-align:center middle;
        }
        .change {
            color:green;
        }
        .hidden {
            display:none;
        }
    }
    """

    def __init__(self, stat: STATS_LITERAL, value: int):
        self.stat = stat
        self.value = value
        super().__init__(id=f"stat_display_{self.stat}")

    def compose(self) -> Iterable[Widget]:
        self.border_title = self.stat
        self.styles.border_title_color = "red"

        yield Digits(value=f"{self.value}", id=f"stat_{self.stat}")
        yield Digits(
            value=f"{self.change_value}",
            id=f"stat_change_{self.stat}",
            classes="change hidden",
        )

        if PROFESSION_MAINSTAT_DICT[self.app.character.profession] == self.stat:
            self.highlight_main_stat()
        return super().compose()

    def highlight_main_stat(self):
        self.border_subtitle = "Main Attribute"
        self.styles.border_subtitle_color = "yellow"

    def watch_change_value(self):
        if self.change_value == 0:
            self.query_one(f"#stat_change_{self.stat}", Digits).add_class("hidden")

        elif self.change_value > 0:
            self.query_one(f"#stat_change_{self.stat}", Digits).remove_class("hidden")
            self.query_one(f"#stat_change_{self.stat}", Digits).update(
                f"+{self.change_value}"
            )

    def watch_added_value(self):
        self.value += self.added_value
        self.added_value = 0
        self.query_one(f"#stat_{self.stat}", Digits).update(f"{self.value}")
