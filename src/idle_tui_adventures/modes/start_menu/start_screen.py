from typing import Iterable, TYPE_CHECKING

from textual import on
from textual.widget import Widget
from textual.screen import Screen
from textual.widgets import Button, Checkbox

from idle_tui_adventures.modes.start_menu.new_character_screen import CharacterCreation
from idle_tui_adventures.modes.start_menu.load_character_screen import (
    CharacterSelection,
)

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure


class StartScreen(Screen):
    app: 'IdleAdventure'
    name: str = "StartScreen"
    DEFAULT_CSS = """StartScreen {
        align: center middle;

        Button {
            width: 33%;
        }
        Checkbox {
            width: 33%;
        }

    }

    """

    def compose(self) -> Iterable[Widget]:
        yield Button("New Character", id="btn_move_to_character_creation")
        yield Button("Load Character", id="btn_move_to_load_character")
        yield Checkbox(
            value=self.app.cfg.skip_screen,
            label="Start on Main Screen",
            tooltip="If checked and there is an active character, the App starts on the Main Screen",
        )

        return super().compose()

    @on(Button.Pressed, "#btn_move_to_character_creation")
    def open_character_creation_screen(self) -> None:
        self.log.debug('Pressed "New Character" Button')
        self.app.push_screen(CharacterCreation())

    @on(Button.Pressed, "#btn_move_to_load_character")
    def open_load_character_screen(self) -> None:
        self.log.debug('Pressed "Load Character" Button')
        self.app.push_screen(CharacterSelection())

    @on(Checkbox.Changed)
    def change_skip_screen_behaviour(self, event: Checkbox.Changed):
        self.log.debug("Changed Skip Screen Behaviour")
        self.app.cfg.skip_screen = event.value
