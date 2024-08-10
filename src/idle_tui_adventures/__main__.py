from idle_tui_adventures.app import IdleAdventure
from idle_tui_adventures.config import init_new_config
from idle_tui_adventures.database.db_utils import init_new_db


def run():
    init_new_db()
    init_new_config()
    app = IdleAdventure()
    app.run()
