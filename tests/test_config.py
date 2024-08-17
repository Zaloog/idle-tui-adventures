from idle_tui_adventures.config import IdleTuiConfig


def test_init_new_config(test_app_config, test_config_file_path):
    assert "database" in test_app_config.config.sections()
    assert "character.active" in test_app_config.config.sections()
    assert test_config_file_path.exists()

    assert test_app_config.active_character_id == 1
    assert not test_app_config.skip_screen
    assert test_app_config.show_damage


def test_IdleTuiConfig(test_app_config, test_config_file_path):
    test_app_config.active_character_id = 1
    test_app_config.skip_screen = True
    test_app_config.show_damage = False

    assert test_app_config.active_character_id == 1
    assert test_app_config.skip_screen
    assert not test_app_config.show_damage

    updated_cfg = IdleTuiConfig(config_path=test_config_file_path)
    assert updated_cfg.active_character_id == 1
    assert updated_cfg.skip_screen
    assert not updated_cfg.show_damage
