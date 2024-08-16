# Todo

- Tests
    - Test DB and Stuff
    - must turn show damage of in tests, otherwise pytest gets stuck,
    if animation i.e. attackspeed is too fast

- Database
    - Struktur
- Classes
    - Character Class
        - Items Equipped
            - query function
        - Inventory
            - query function
        - Stats
            - Calculated
                - Total Str, Int, Dex, Luc
                - Crit Rate
                - Crit Damage
                - Chance item find
                - Mana
                - Hp
                - Attack Speed
                - Damage
    - Equip Class
        - Damage
        - Stat Bonuses
        - Equip SubClasses
            - Weapon
            - Shield
            - Helmet
            - Armor
            - Boots
            - Rings

- Start Screen
    - new character creation
        - Background
    - load character screen
        - horizontal scroll character view
            - Options popup
                - Rename
                - Delete

- Main Screen
    - Layout define
        - Monster Screen
            - Monster spawn
            - Monster class multiply stats based on current gamestate
            - Monster Stat DB?
        - Stages?
            - Stage X/1 -> X/10 -> Boss -> X+1/1...
    - Shop Screen
        - Buy/Sell Stuff?
    - Equip Move Popup
        - character stats
            - define db schema
            - drag n drop
                - update in db
                - tool tip item stats

- Settings Screen
    - Statistics?
    - DB Location
    - show damage
