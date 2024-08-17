from idle_tui_adventures.app import IdleAdventure
from idle_tui_adventures.config import init_new_config


def run():
    init_new_config()
    app = IdleAdventure()
    app.run()
