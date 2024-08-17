from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure


from textual import on
from textual.events import Mount, ScreenResume
from textual.widget import Widget
from textual.widgets import Placeholder
from textual.screen import ModalScreen

from idle_tui_adventures.widgets.icon_widgets import MenuIconsRow
from idle_tui_adventures.widgets.character_screen_widgets import CharacterInterface


class CharacterScreen(ModalScreen):
    app: "IdleAdventure"
    name: str = "CharacterScreen"
    BINDINGS = [("escape", "app.pop_screen"), ("c", "app.pop_screen")]

    def compose(self) -> Iterable[Widget]:
        yield CharacterInterface()
        yield Placeholder("Equipment")
        yield MenuIconsRow()
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        self.query_one("#character").add_class("-active")
        self.log.error("set to active")
        return super()._on_mount(event)

    @on(ScreenResume)
    def update_character_interface(self):
        self.query_one(
            CharacterInterface
        ).unassigned_stat_points = self.app.character.unassigned_stat_points
        self.query_one(CharacterInterface).spent_stat_dict = {
            stat: 0 for stat in self.query_one(CharacterInterface).spent_stat_dict
        }
        self.query_one(CharacterInterface).mutate_reactive(
            CharacterInterface.spent_stat_dict
        )

        self.query_one(MenuIconsRow).focus()
