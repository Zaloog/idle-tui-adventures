import pytest

from idle_tui_adventures.constants import CONFIG_NAME, DB_NAME
from idle_tui_adventures.config import init_new_config, IdleTuiConfig
from idle_tui_adventures.database.db_utils import init_new_db
from idle_tui_adventures.database.db_transactions import create_new_character_db
from idle_tui_adventures.app import IdleAdventure


@pytest.fixture
def test_config_path(tmp_path):
    return tmp_path


@pytest.fixture
def test_config_file_path(test_config_path):
    return test_config_path / CONFIG_NAME


@pytest.fixture
def test_app_config(test_config_file_path) -> IdleTuiConfig:
    init_new_config(conf_path=test_config_file_path)

    cfg = IdleTuiConfig(config_path=test_config_file_path)
    return cfg


@pytest.fixture
def test_db_path(tmp_path):
    return tmp_path


@pytest.fixture
def test_db_file_path(test_db_path):
    return test_db_path / DB_NAME


@pytest.fixture
def init_test_db(test_db_file_path):
    init_new_db(database=test_db_file_path)

    create_new_character_db(
        name="Test",
        profession="Warrior",
        strength=0,
        intelligence=0,
        dexterity=0,
        luck=0,
    )


@pytest.fixture
def TestApp():
    return IdleAdventure()
