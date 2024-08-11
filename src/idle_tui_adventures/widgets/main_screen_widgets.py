from __future__ import annotations
from typing import Coroutine, Any, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from random import randint, random

from textual import on
from textual.geometry import Offset
from textual.message import Message
from textual.events import Click, Compose, Mount
from textual.widget import Widget
from textual.widgets import ProgressBar, Label, Digits
from textual.containers import Vertical

from idle_tui_adventures.utils import calculate_exp_needed
from idle_tui_adventures.constants import MONSTER_PER_STAGE
from idle_tui_adventures.widgets.icon_widgets import ImageStatic
from idle_tui_adventures.database.db_transactions import (
    update_minor_stage_db,
    update_major_stage_db,
)


class CharacterProgressbar(ProgressBar):
    app: "IdleAdventure"

    DEFAULT_CSS = """
    CharacterProgressbar {
        column-span: 5;
        row-span: 1;
        width: 1fr;
        height: 3;
        align: center middle;
        layer: above;
        offset: 0 300%;

        & Bar  {
            width: 1fr;
            }

        & Bar > .bar--bar {
            color: blue;
            }

        & PercentageStatus {
        width: 5;
        align: center middle;
        offset: -50vw 0;
        }
    }
"""

    def __init__(
        self,
        show_percentage: bool = True,
        show_eta: bool = False,
    ):
        super().__init__(show_percentage=show_percentage, show_eta=show_eta)

    def _on_compose(self, event: Compose) -> Coroutine[Any, Any, None]:
        self.timer = self.set_interval(1 / 10, self.make_progress, pause=True)
        return super()._on_compose(event)

    def on_mount(self) -> None:
        if self.app.character:
            new_total = calculate_exp_needed(next_lvl=self.app.character.level + 1)
            last_total = calculate_exp_needed(next_lvl=self.app.character.level)
            current_exp = self.app.character.experience - last_total

            self.update(progress=current_exp, total=new_total - last_total)
            self.timer.resume()
        return super().on_mount()

    def make_progress(self):
        self.update(advance=1)
        self.app.character.collect_exp()
        if self.percentage == 1:
            self.advance_level()

    def advance_level(self):
        self.app.character.level_up()
        self.notify(
            title="Level Up",
            message=f"{self.app.character.name} reached level [blue]{self.app.character.level}[/]",
            timeout=1,
        )
        new_total = calculate_exp_needed(next_lvl=self.app.character.level + 1)
        last_total = calculate_exp_needed(next_lvl=self.app.character.level)
        self.update(progress=0, total=new_total - last_total)


class HealthBar(ProgressBar):
    app: "IdleAdventure"
    DEFAULT_CSS = """
    HealthBar {
    height: auto;

    & Bar  {
        width: 1fr;
        }

    & Bar > .bar--bar {
        color: red;
        }
    }
    """

    class HpReachedZero(Message):
        def __init__(self, healthbar: HealthBar):
            self.healthbar = healthbar
            super().__init__()

        @property
        def control(self) -> HealthBar:
            return self.healthbar

    def __init__(self, max_hp: int, id: str | None = None):
        self.max_hp = max_hp
        super().__init__(
            total=self.max_hp, show_percentage=False, show_eta=False, id=id
        )

        self.update(progress=self.max_hp)

    def heal(self, amount: int):
        self.progress += amount

    def damage(self, amount: int):
        self.progress -= amount
        if self.progress <= 0:
            self.post_message(self.HpReachedZero(self))
            self.heal_to_full()

    def heal_to_full(self):
        self.progress = self.total


class MonsterPanel(Vertical):
    app: "IdleAdventure"
    DEFAULT_CSS = """
    MonsterPanel {
        row-span: 3;
        column-span: 2;
        width: 1fr;
        height: 1fr;

        HealthBar {
            height: auto;
        }

        & ImageStatic {
            width: 1fr;
            height: 1fr;
        }
        & #label_monster_name {
            text-align:center;
            width: 1fr;
        }
    }
    """

    class MonsterDefeated(Message):
        def __init__(self, monster_panel: MonsterPanel):
            self.monster_panel = monster_panel
            super().__init__()

        @property
        def control(self) -> MonsterPanel:
            return self.monster_panel

    def compose(self) -> Iterable[Widget]:
        yield Label("Monster Bad", id="label_monster_name")
        yield HealthBar(max_hp=1_000)
        yield ImageStatic(icon_name="dragon")

        return super().compose()

    def _on_compose(self, event: Compose) -> Coroutine[Any, Any, None]:
        self.timer = self.set_interval(
            interval=1 / self.app.character.attack_speed,
            callback=self.fight_monster,
        )

        return super()._on_compose(event)

    def fight_monster(self):
        damage = self.app.character.damage
        try:
            self.mount(DamageLabel(damage=damage, parent_size=self.size))
        except Exception:
            pass
        self.query_one(HealthBar).damage(damage)

    @on(HealthBar.HpReachedZero)
    def monster_is_dead(
        self,
    ):
        self.post_message(self.MonsterDefeated(self))

    def _on_click(self, event: Click) -> Coroutine[Any, Any, None]:
        self.fight_monster()
        return super()._on_click(event)


class StageDisplay(Vertical):
    app: "IdleAdventure"
    DEFAULT_CSS = """
    StageDisplay {
        height: auto;
        width:1fr;
        align:center middle;

        & Label {
            width:1fr;
            text-align: center;
        }
        & Digits {
            width:1fr;
            text-align: center;
        }
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.stage_string = (
            f"{self.app.gamestate.major_stage} - {self.app.gamestate.minor_stage}"
        )

    def compose(self) -> Iterable[Widget]:
        yield Label("Current Stage")
        yield Digits(value=self.stage_string)
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.stage_string = (
            f"{self.app.gamestate.major_stage} - {self.app.gamestate.minor_stage}"
        )
        return super()._on_mount(event)

    def advance_stage(self) -> None:
        if self.app.gamestate.minor_stage == MONSTER_PER_STAGE:
            self.app.gamestate.major_stage += 1
            self.app.gamestate.minor_stage = 1
            update_major_stage_db(
                gamestate_id=self.app.gamestate.gamestate_id,
                major_stage=self.app.gamestate.major_stage,
            )
        else:
            self.app.gamestate.minor_stage += 1
        self.query_one(Digits).update(
            f"{self.app.gamestate.major_stage} - {self.app.gamestate.minor_stage}"
        )
        update_minor_stage_db(
            gamestate_id=self.app.gamestate.gamestate_id,
            minor_stage=self.app.gamestate.minor_stage,
        )


class DamageLabel(Label):
    DEFAULT_CSS = """
    DamageLabel {
        layer:above;
        color:red;
        text_align:center;
        width:auto;
        background:black;

    }
    """

    def __init__(self, damage: int, parent_size: Offset) -> None:
        self.damage = damage
        self.wiggle = randint(-10, 10)

        self.parent_center = Offset(
            parent_size[0] // 2 + self.wiggle, parent_size[1] // 2
        )

        super().__init__(renderable=f"{damage}")

        if random() <= self.app.character.crit_rate:
            self.styles.border = "outer", "red"
            self.update(f"CRIT {self.damage}")

        self.offset = self.parent_center
        self.fly_away()

    def fly_away(self):
        self.styles.animate(
            attribute="opacity",
            value=0,
            duration=1.5,
        )

        self.animate(
            attribute="offset",
            value=Offset(self.parent_center[0] + self.wiggle, 0),
            duration=1.0,
            on_complete=self.remove,
            easing="out_expo",
        )
