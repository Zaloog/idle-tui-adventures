import pytest

SCREEN_SIZE = (80, 120)
IMAGE_CLICK_OFFSET = (2, 2)


@pytest.mark.asyncio
async def test_mode_switches(TestApp):
    async with TestApp.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("1")
        assert TestApp.screen.name == "StartScreen"

        await pilot.press("2")
        assert TestApp.screen.name == "MainScreen"

        await pilot.press("3")
        assert TestApp.screen.name == "SettingsScreen"


@pytest.mark.asyncio
async def test_start_screen_buttons(TestApp):
    async with TestApp.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("1")
        await pilot.click("#btn_move_to_character_creation", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "CharacterCreation"

        await pilot.press("escape")
        assert TestApp.screen.name == "StartScreen"

        await pilot.click("#btn_move_to_load_character")
        assert TestApp.screen.name == "CharacterSelection"

        await pilot.press("escape")
        assert TestApp.screen.name == "StartScreen"


@pytest.mark.asyncio
async def test_move_to_character_screen(TestApp):
    async with TestApp.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        # From main
        await pilot.press("c")
        assert TestApp.screen.name == "CharacterScreen"
        # Close
        await pilot.click("#character", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "MainScreen"
        await pilot.click("#character", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "CharacterScreen"
        await pilot.press("l")
        assert TestApp.screen.name == "ShopScreen"
        # From other
        await pilot.press("c")
        assert TestApp.screen.name == "CharacterScreen"


@pytest.mark.asyncio
async def test_move_to_backpack_screen(TestApp):
    async with TestApp.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        # from Main
        await pilot.click("#backpack", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "InventoryEquipScreen"
        # close
        await pilot.press("b")
        assert TestApp.screen.name == "MainScreen"
        await pilot.click("#backpack", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "InventoryEquipScreen"
        await pilot.press("c")
        assert TestApp.screen.name == "CharacterScreen"
        # From other
        await pilot.click("#backpack", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "InventoryEquipScreen"


@pytest.mark.asyncio
async def test_move_to_dungeon_screen(TestApp):
    async with TestApp.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        # from Main
        await pilot.press("d")
        assert TestApp.screen.name == "DungeonScreen"
        await pilot.click("#shop", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "ShopScreen"
        # from other
        await pilot.pause(delay=0.5)
        await pilot.press("d")
        assert TestApp.screen.name == "DungeonScreen"
        # close
        await pilot.click("#dungeon", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "MainScreen"
        await pilot.click("#dungeon", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "DungeonScreen"


@pytest.mark.asyncio
async def test_move_to_shop_screen(TestApp):
    async with TestApp.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        # from main
        await pilot.click("#shop", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "ShopScreen"
        await pilot.pause(delay=0.5)
        await pilot.press("c")
        assert TestApp.screen.name == "CharacterScreen"
        await pilot.click("#dungeon", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "DungeonScreen"
        # from other
        await pilot.press("l")
        assert TestApp.screen.name == "ShopScreen"
        # close
        await pilot.press("l")
        assert TestApp.screen.name == "MainScreen"


@pytest.mark.asyncio
async def test_move_to_settings(TestApp):
    async with TestApp.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        await pilot.press("b")
        assert TestApp.screen.name == "InventoryEquipScreen"
        await pilot.click("#settings", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "SettingsScreen"
        await pilot.press("2")
        assert TestApp.screen.name == "InventoryEquipScreen"
        await pilot.click("#backpack", offset=IMAGE_CLICK_OFFSET)
        assert TestApp.screen.name == "MainScreen"
        await pilot.press("3")
        assert TestApp.screen.name == "SettingsScreen"
