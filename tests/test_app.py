import pytest

from idle_tui_adventures.app import IdleAdventure

SCREEN_SIZE = (80, 120)


@pytest.mark.asyncio
async def test_mode_switches():
    app = IdleAdventure()

    async with app.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("1")
        assert app.screen.name == "StartScreen"

        await pilot.press("2")
        assert app.screen.name == "MainScreen"

        await pilot.press("3")
        assert app.screen.name == "SettingsScreen"


@pytest.mark.asyncio
async def test_start_screen_buttons():
    app = IdleAdventure()

    async with app.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("1")
        await pilot.click("#btn_move_to_character_creation")
        assert app.screen.name == "CharacterCreation"

        await pilot.press("escape")
        assert app.screen.name == "StartScreen"

        await pilot.click("#btn_move_to_load_character")
        assert app.screen.name == "CharacterSelection"

        await pilot.press("escape")
        assert app.screen.name == "StartScreen"


@pytest.mark.asyncio
async def test_move_to_character_screen():
    app = IdleAdventure()

    async with app.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        await pilot.press("c")
        assert app.screen.name == "CharacterScreen"
        await pilot.click("#character")
        assert app.screen.name == "MainScreen"
        await pilot.click("#character")
        assert app.screen.name == "CharacterScreen"
        await pilot.press("l")
        assert app.screen.name == "ShopScreen"
        await pilot.press("c")
        assert app.screen.name == "CharacterScreen"


@pytest.mark.asyncio
async def test_move_to_backpack_screen():
    app = IdleAdventure()

    async with app.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        await pilot.click("#backpack")
        assert app.screen.name == "InventoryEquipScreen"
        await pilot.press("b")
        assert app.screen.name == "MainScreen"
        await pilot.click("#backpack")
        assert app.screen.name == "InventoryEquipScreen"
        await pilot.press("c")
        assert app.screen.name == "CharacterScreen"
        await pilot.click("#backpack")
        assert app.screen.name == "InventoryEquipScreen"


@pytest.mark.asyncio
async def test_move_to_dungeon_screen():
    app = IdleAdventure()

    async with app.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        await pilot.press("d")
        assert app.screen.name == "DungeonScreen"
        await pilot.click("#shop")
        assert app.screen.name == "ShopScreen"
        await pilot.press("d")
        assert app.screen.name == "DungeonScreen"
        await pilot.click("#dungeon")
        assert app.screen.name == "MainScreen"
        await pilot.click("#dungeon")
        assert app.screen.name == "DungeonScreen"


@pytest.mark.asyncio
async def test_move_to_shop_screen():
    app = IdleAdventure()

    async with app.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        await pilot.click("#shop")
        assert app.screen.name == "ShopScreen"
        await pilot.press("c")
        assert app.screen.name == "CharacterScreen"
        await pilot.click("#dungeon")
        assert app.screen.name == "DungeonScreen"
        await pilot.press("l")
        assert app.screen.name == "ShopScreen"
        await pilot.press("l")
        assert app.screen.name == "MainScreen"


@pytest.mark.asyncio
async def test_move_to_settings():
    app = IdleAdventure()

    async with app.run_test(size=SCREEN_SIZE) as pilot:
        await pilot.press("2")

        await pilot.press("b")
        assert app.screen.name == "InventoryEquipScreen"
        await pilot.click("#settings")
        assert app.screen.name == "SettingsScreen"
        await pilot.press("2")
        assert app.screen.name == "InventoryEquipScreen"
        await pilot.click("#backpack")
        assert app.screen.name == "MainScreen"
        await pilot.press("3")
        assert app.screen.name == "SettingsScreen"
