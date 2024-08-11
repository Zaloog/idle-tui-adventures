from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure

from textual import on
from textual.widget import Widget
from textual.widgets import Placeholder
from textual.screen import Screen

from idle_tui_adventures.widgets.main_screen_widgets import (
    CharacterProgressbar,
    MonsterPanel,
    StageDisplay,
)
from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow
from idle_tui_adventures.database.db_transactions import update_monsters_killed_db


class MainScreen(Screen):
    app: "IdleAdventure"
    monster_killed: int = 0
    name: str = "MainScreen"
    DEFAULT_CSS = """MainScreen {
        layout: grid;
        grid-size: 3 4;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1;
        align: center middle;
    }

    """

    def compose(self) -> Iterable[Widget]:
        yield Placeholder("Character", id="tile_0")
        yield MonsterPanel()
        yield StageDisplay()
        yield Placeholder("Log", id="tile_2")

        yield CharacterProgressbar()
        yield MenuIconsRow()

        return super().compose()

    # @on(ScreenSuspend)
    # def pause_progress(self):
    #     p_bar = self.query_one(CharacterProgressbar)
    #     p_bar.timer.pause()
    #     monster = self.query_one(MonsterPanel)
    #     monster.timer.pause()

    # @on(ScreenResume)
    # def recalibrate_progressbar(self):
    #     if self.app.character:
    #         new_total = calculate_exp_needed(next_lvl=self.app.character.level + 1)
    #         last_total = calculate_exp_needed(next_lvl=self.app.character.level)
    #         current_exp = self.app.character.experience - last_total

    #         p_bar = self.query_one(CharacterProgressbar)
    #         p_bar.update(progress=current_exp, total=new_total - last_total)
    #         p_bar.timer.resume()
    #         monster = self.query_one(MonsterPanel)
    #         monster.timer.resume()

    @on(MonsterPanel.MonsterDefeated)
    def advance_stage(self):
        self.monster_killed += 1
        update_monsters_killed_db(gamestate_id=self.app.gamestate.gamestate_id)
        if self.monster_killed == 5:
            self.monster_killed = 0
            self.query_one(MonsterPanel).refresh(recompose=True, repaint=False)
            self.query_one(StageDisplay).advance_stage()
