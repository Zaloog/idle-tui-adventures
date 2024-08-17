from sqlite3 import Row
from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from idle_tui_adventures.app import IdleAdventure


from textual import on
from textual.events import Mount
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.containers import HorizontalScroll
from textual.widgets import Button

from idle_tui_adventures.database.db_queries import (
    get_all_characters,
    get_stages_for_character,
)
from idle_tui_adventures.widgets.icon_widgets import CharacterPreview
from idle_tui_adventures.modes.main_menu.main_screen import MainScreen
from idle_tui_adventures.modes.main_menu.character_screen import CharacterScreen
from idle_tui_adventures.modes.main_menu.inventory_screen import InventoryEquipScreen
from idle_tui_adventures.modes.main_menu.shop_screen import ShopScreen


class CharacterSelection(ModalScreen):
    app: "IdleAdventure"
    name: str = "CharacterSelection"
    BINDINGS = [("escape", "app.pop_screen")]

    def compose(self) -> Iterable[Widget]:
        self.characters: list[Row] = get_all_characters(
            database=self.app.cfg.database_path
        )
        with HorizontalScroll():
            for char_data in self.characters:
                stage_data = get_stages_for_character(
                    character_id=dict(char_data)["character_id"],
                    database=self.app.cfg.database_path,
                )
                yield CharacterPreview(character_data=char_data, stage_data=stage_data)
        yield Button("Start Adventure", id="btn_start_adventure")
        yield Button("Back to Start Screen", id="btn_go_back")
        return super().compose()

    def _on_mount(self, event: Mount) -> None:
        try:
            self.query_one(
                f"#character_id_{self.app.cfg.active_character_id}"
            ).add_class("-active")
            self.app.load_active_character()
        except Exception:
            self.query_one("#btn_start_adventure", Button).disabled = True
            self.notify(
                title="No active character available",
                message="Please create your first character",
                severity="error",
                timeout=2,
            )
        return super()._on_mount(event)

    @on(Button.Pressed, "#btn_start_adventure")
    def move_to_main_screen(self):
        self.dismiss()
        self.app.switch_mode("Main")

    @on(Button.Pressed, "#btn_go_back")
    def move_to_start_screen(self):
        self.dismiss()

    @on(CharacterPreview.SelectOther)
    def only_highlight_clicked(self, event: CharacterPreview.SelectOther) -> None:
        # remove active class from other Widgets
        self.app.cfg.active_character_id = event.character_preview.id.split("_")[-1]
        self.app.load_active_character()
        self.query(CharacterPreview).exclude(
            f"#{event.character_preview.id}"
        ).remove_class("-active")

        # reload all screens on Character Switch
        self.app.remove_mode("Main")
        self.app.add_mode(mode="Main", base_screen=MainScreen)

        self.app.uninstall_screen("CharacterScreen")
        self.app.install_screen(screen=CharacterScreen, name="CharacterScreen")

        self.app.uninstall_screen("InventoryEquipScreen")
        self.app.install_screen(
            screen=InventoryEquipScreen, name="InventoryEquipScreen"
        )

        self.app.uninstall_screen("ShopScreen")
        self.app.install_screen(screen=ShopScreen, name="ShopScreen")
