import pytest

from idle_tui_adventures.constants import CONFIG_NAME
from idle_tui_adventures.config import init_new_config, IdleTuiConfig


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
