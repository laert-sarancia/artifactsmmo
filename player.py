import asyncio
from datetime import datetime
from base_api import API

CRAFT_ITEMS = {
    "cooking": {
        0: ["cooked_gudgeon"],
        5: ["cooked_gudgeon"],
        10: ["cooked_shrimp", "beef_stew", "mushroom_soup", "fried_eggs"],
        15: ["cooked_shrimp", "cooked_wolf_meat", "fried_eggs"],
        20: ["cooked_trout", "cheese", "cooked_wolf_meat"],
        25: ["cooked_trout", "cooked_wolf_meat", "cheese"],
        30: ["cooked_trout", "mushroom_soup", "beef_stew"],
    },
    "weaponcrafting": {
        0: ["copper_dagger", "wooden_staff"],
        5: ["fire_staff", "sticky_dagger", "sticky_sword", "water_bow"],
        10: ["iron_dagger", "greater_wooden_staff"],
        15: ["mushstaff", "mushmush_bow", "multislimes_sword"],
        20: ["battlestaff", "steel_axe", "battlestaff", "steel_axe",
             "battlestaff", "steel_axe", "skull_staff", "forest_whip", ],
        25: ["skull_wand", "dreadful_staff"],
        30: ["gold_sword", "greater_dreadful_staff"],
    },
    "gearcrafting": {
        0: ["copper_boots"],
        5: ["copper_armor", "copper_legs_armor", "feather_coat"],
        10: ["iron_boots", "iron_boots", "iron_boots", "iron_helm"],
        15: ["magic_wizard_hat", "steel_helm", "steel_boots", "steel_armor"],
        20: ["magic_wizard_hat", "steel_helm", "steel_boots", "steel_armor"],
        25: ["magic_wizard_hat", "steel_helm", "steel_boots", "steel_armor"],
        30: ["magic_wizard_hat", "steel_helm", "steel_boots", "steel_armor"],
    },
    "jewelrycrafting": {
        0: ["copper_ring"],
        5: ["life_amulet"],
        10: ["iron_ring"],
        15: ["life_ring", "air_ring", "earth_ring", "fire_ring", "water_ring"],
        20: ["steel_ring", "ring_of_chance", "dreadful_ring", "skull_ring", ],
        25: ["gold_ring", "topaz_ring", "sapphire_ring", "emerald_ring"],
        30: ["gold_ring", "topaz_ring", "sapphire_ring", "emerald_ring"],
    },
}


def wait(func):
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        if response:
            cooldown = response.get("cooldown", {}).get("total_seconds", 0)
            await asyncio.sleep(cooldown)
        return response

    return wrapper


class Player(API):
    def __init__(self, name: str, game):
        self.name = name
        self.game = game
        self.character = self.get_character()

    def __repr__(self) -> str:
        return self.name

# ******* BASIC ACTIONS ****** #

    @wait
    async def move(self, x: int, y: int) -> dict | list:
        if self.character.get("x") != x or self.character.get("y") != y:
            response = self.post(
                endpoint=f"/my/{self.name}/action/move",
                data={"x": x, "y": y}
            )
            character = response.get("character")
            if character:
                self.character = character
            else:
                print(f"NO CHARACTER IN RESPONSE ({self.name})")
            return response

    @wait
    async def gathering(self) -> dict | list:
        response = self.post(f"/my/{self.name}/action/gathering")
        if response:
            character = response.get("character")
            if character:
                self.character = character
            else:
                print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def crafting(self, code: str, quantity: int = 1) -> dict | list:
        response = self.post(
            endpoint=f"/my/{self.name}/action/crafting",
            data={"code": code, "quantity": quantity}
        )
        character = response.get("character")
        if character:
            self.character = character
        else:
            print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def equip(self, code: str, slot: str) -> dict | list:
        if self.character.get(f"{slot}_slot"):
            await self.unequip(slot)
        response = self.post(
            endpoint=f"/my/{self.name}/action/equip",
            data={"code": code, "slot": slot}
        )
        character = response.get("character")
        if character:
            self.character = character
        else:
            print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def unequip(self, slot: str) -> dict | list:
        response = self.post(
            endpoint=f"/my/{self.name}/action/unequip",
            data={"slot": slot}
        )
        character = response.get("character")
        if character:
            self.character = character
        else:
            print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def sell(self, code: str, quantity: int = 1) -> dict | list:
        await self.move(5, 1)
        price = self.game.get_item(code).get("ge").get("sell_price")
        response = self.post(
            endpoint=f"/my/{self.name}/action/ge/sell",
            data={"code": code,
                  "quantity": quantity,
                  "price": price}
        )
        character = response.get("character")
        if character:
            self.character = character
        else:
            print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def deposit_item(self, code: str, quantity: int = 1) -> dict | list:
        endpoint = f"/my/{self.name}/action/bank/deposit"
        await self.move(4, 1)
        if self.count_inventory_item(code):
            if self.count_inventory_item(code) < quantity:
                response = self.post(
                    endpoint=endpoint,
                    data={"code": code,
                          "quantity": self.count_inventory_item(code)}
                )
            else:
                response = self.post(
                    endpoint=endpoint,
                    data={"code": code,
                          "quantity": quantity}
                )
            character = response.get("character")
            if character:
                self.character = character
            else:
                print(f"NO CHARACTER IN RESPONSE ({self.name})")
            return response

    @wait
    async def withdraw_item(self, code: str, quantity: int = 1) -> dict | list:
        endpoint = f"/my/{self.name}/action/bank/withdraw"
        bank = [it for it in self.game.get_bank_items(code) if it.get("code") == code]
        if bank:
            await self.move(4, 1)
            if bank[0].get("quantity") <= quantity:
                response = self.post(
                    endpoint=endpoint,
                    data={"code": code,
                          "quantity": bank[0].get("quantity")}
                )
            else:
                response = self.post(
                    endpoint=endpoint,
                    data={"code": code,
                          "quantity": quantity}
                )
            character = response.get("character")
            if character:
                self.character = character
            else:
                print(f"NO CHARACTER IN RESPONSE ({self.name})")
            return response
        else:
            print(f"No items {code} ({self.name})")
            return {}

    @wait
    async def recycling(self, code: str, quantity: int = 1) -> dict | list:
        response = self.post(
            endpoint=f"/my/{self.name}/action/recycling",
            data={
                "code": code,
                "quantity": quantity
            }
        )
        character = response.get("character")
        if character:
            self.character = character
        else:
            print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def fight(self) -> dict | list:
        response = self.post(endpoint=f"/my/{self.name}/action/fight")
        if response:
            character = response.get("character")
            if character:
                self.character = character
            else:
                print(f"NO CHARACTER IN RESPONSE ({self.name})")
                return {}
            fight_result = response.get("fight")
            if fight_result.get("result") == "lose":
                print(f"Monster too strong for {self.name}")
                return {}
            elif fight_result.get("drops"):
                drops = [f'{item["quantity"]} {item["code"]}' for item in fight_result.get("drops")]
                print(f'Won {", ".join(drops)} ({self.name})')
            return response
        else:
            return {}

    @wait
    async def new_task(self) -> dict | list:
        await self.move(1, 2)
        response = self.post(endpoint=f"/my/{self.name}/action/task/new")
        return response

    @wait
    async def complete_task(self) -> dict | list:
        await self.move(1, 2)
        response = self.post(endpoint=f"/my/{self.name}/action/task/complete")
        return response

    @wait
    async def task_exchange(self) -> dict | list:
        await self.move(1, 2)
        if self.check_item_on("tasks_coin"):
            if self.count_inventory_item("tasks_coin") > 2:
                response = self.post(endpoint=f"/my/{self.name}/action/task/exchange")
                character = response.get("character")
                if character:
                    self.character = character
                else:
                    print(f"NO CHARACTER IN RESPONSE ({self.name})")
                return response

    def get_character(self) -> dict | list:
        response = self.get(endpoint=f"/characters/{self.name}")
        return response

    def get_slot_of_equip(self, code: str) -> str:
        equip: list = [slot for slot in self.character if "_slot" in slot and self.character[slot] == code]
        if equip:
            return equip[0].rstrip("_slot")
        else:
            print(f"No equip {code} on {self.name}")

    def get_slot_of_item(self, code: str) -> str:
        inventory = self.character.get("inventory")
        slot = [slot["slot"] for slot in inventory if slot["code"] == code]
        return slot[0]

    def check_item_on(self, code: str) -> bool:
        inventory = self.character.get("inventory")
        if [slot for slot in inventory if slot["code"] == code]:
            return True
        return False

    def count_inventory_item(self, code: str) -> int:
        inventory = self.character.get("inventory")
        if self.check_item_on(code):
            qty = [slot["quantity"] for slot in inventory if slot["code"] == code]
            if qty:
                return sum(qty)
        else:
            return 0

    # ******* COMPLEX ACTIONS ****** #

    async def gathering_items(self, code: str, quantity: int = 1):
        weapon = self.character.get("weapon_slot")
        subtype = self.game.items[code].get("subtype")
        if subtype == "mining":
            tool = "iron_pickaxe"
        elif subtype == "woodcutting":
            tool = "iron_axe"
        elif subtype == "fishing":
            tool = "spruce_fishing_rod"
        else:
            tool = None
            print(f"Incorrect subtype {subtype} ({self.name})")
        if self.character.get("weapon_slot") != tool:
            await self.withdraw_item(tool)
            await self.equip(tool, "weapon")
            await self.deposit_item(weapon)
        if code == "copper_ore":
            await self.move(2, 0)
        elif code == "iron_ore":
            await self.move(1, 7)
        elif code == "coal":
            await self.move(1, 6)
        elif code == "gold_ore":
            await self.move(10, -4)
        elif code == "ash_wood":
            await self.move(-1, 0)
        elif code == "spruce_wood":
            await self.move(2, 6)
        elif code == "birch_wood":
            await self.move(3, 5)
        elif code == "dead_wood":
            await self.move(9, 8)
        elif code == "gudgeon":
            await self.move(4, 2)
        elif code == "shrimp":
            await self.move(5, 2)
        elif code == "trout":
            await self.move(-2, 6)
        elif code == "bass":
            await self.move(-3, 6)
        while not self.check_item_on(code):
            await self.gathering()
        while self.count_inventory_item(code) < quantity:
            await self.gathering()

    async def craft_item_scenario(self, code: str, quantity: int = 1):
        if self.count_inventory_item(code) < quantity:
            craft = self.game.items[code].get("craft")
            if craft:
                skill, level, components, qty = craft.values()
                for item in components:
                    item_code = item.get("code")
                    item_quantity = item.get("quantity")
                    bank = [it for it in self.game.get_bank_items(item_code) if it.get("code") == item_code]
                    if bank:
                        if bank[0].get("quantity") > item_quantity * quantity:
                            await self.withdraw_item(item_code, item_quantity * quantity)
                        else:
                            await self.withdraw_item(item_code, bank[0].get("quantity"))
                    if self.count_inventory_item(item_code) < item_quantity * quantity:
                        await self.craft_item_scenario(
                            item_code,
                            item_quantity * quantity - self.count_inventory_item("code"))
                for item in components:
                    item_code = item.get("code")
                    item_quantity = item.get("quantity")
                    if self.count_inventory_item(item_code) < item_quantity * quantity:
                        await self.craft_item_scenario(
                            item_code,
                            item_quantity * quantity - self.count_inventory_item("code"))
                await self.move_to_craft(skill)
                await self.crafting(code, quantity)
            else:
                if self.game.items[code].get("subtype") in ["woodcutting", "fishing", "mining"]:
                    await self.gathering_items(code, quantity)
                else:
                    while self.count_inventory_item(code) < quantity:
                        monsters = self.game.get_monsters(drop=code)
                        if monsters:
                            monster = monsters[0].get("code")
                            await self.kill_monster(monster)
                        else:
                            print(f"No monster here ({self.name})")
                            return 500

    async def move_to_craft(self, skill):
        if skill == "cooking":
            await self.move(1, 1)
        elif skill == "mining":
            await self.move(1, 5)
        elif skill == "weaponcrafting":
            await self.move(2, 1)
        elif skill == "gearcrafting":
            await self.move(3, 1)
        elif skill == "woodcutting":
            await self.move(-2, -3)
        elif skill == "jewelrycrafting":
            await self.move(1, 3)

    async def task_circle(self):
        await self.complete_task()
        await self.new_task()

    async def change_items(self, code: str):
        i_type = self.game.items[code].get("type")
        slot = f'{i_type}'
        bank_items = [item.get("code") for item in self.game.get_bank_items()]
        my_items = [item.get("code") for item in self.character.get("inventory") if item.get("code")]
        all_items = my_items + bank_items
        if code in all_items:
            if not self.count_inventory_item(code):
                await self.withdraw_item(code)
        await self.equip(code, slot)
        await self.drop_all()

    async def kill_monster(self, monster: str, quantity: int = 1):
        monster_stats = self.game.monsters[monster]
        monster_res = {key: value for key, value in monster_stats.items() if "res_" in key}
        min_res: str = min(monster_res, key=monster_res.get)
        el = min_res.replace("res_", "attack_")
        bank_items = [item.get("code") for item in self.game.get_bank_items()]
        my_items = [item.get("code") for item in self.character.get("inventory") if item.get("code")]
        all_items = my_items + bank_items
        weapons = {}
        for weapon in all_items:
            item = self.game.items[weapon]
            if item.get("type") == "weapon" \
                    and item.get("level", 0) <= self.character.get("level"):
                weapons[weapon] = item.get("effects", {})
        best: tuple[int, str | None] = (0, None)
        for weapon, stats in weapons.items():
            for tp in stats:
                if tp["name"] == el:
                    if best[0] < tp["value"]:
                        best = (tp["value"], weapon)
        # TODO Check all slots and change to better item!
        if weapons:
            if self.character.get("weapon_slot") != best[1]:
                if best[1]:
                    await self.change_items(best[1])

        await self.move(**self.game.get_monster_coord(monster))
        for i in range(quantity):
            result = await self.fight()
            if result == {}:
                return 500

    async def do_task(self):
        if self.character.get("task_type") == "monsters":
            monster = self.character.get("task")
            if self.game.monsters[monster].get("level") < self.character.get("level"):
                result = await self.kill_monster(
                    monster,
                    self.character.get("task_total") - self.character.get("task_progress"))
                if result == 500:
                    return 500
                await self.task_circle()
            else:
                print(f"Too hard Task {monster} ({self.name})")

    async def drop_all(self):
        inventory = self.character.get("inventory")
        for slot in reversed(inventory):
            if slot["quantity"]:
                await self.deposit_item(slot["code"], slot["quantity"])

    async def recycling_from_bank(self, code, quantity: int = 1):
        inventory = self.count_inventory_item(code)
        bank = self.game.get_bank_items(code)
        bank = bank[0].get("quantity") if bank else 0

        if inventory < quantity <= bank + inventory:
            await self.withdraw_item(code, quantity - inventory)
        elif quantity > bank + inventory:
            quantity = bank + inventory
            await self.withdraw_item(code, bank)

        await self.move_to_craft(self.game.items[code].get("craft").get("skill"))
        await self.recycling(code, quantity)
        await self.drop_all()

    async def crafter(self):
        if not self.character.get("task"):
            await self.new_task()
        while True:
            bank_items = self.game.get_bank_items("tasks_coin")
            if bank_items:
                coins = bank_items[0].get("quantity")
                if coins > 2:
                    await self.withdraw_item("tasks_coin", coins // 3 * 3)
                    for _ in range(coins // 3):
                        await self.task_exchange()
                    await self.drop_all()
            types = ["weaponcrafting",
                     "gearcrafting",
                     "jewelrycrafting"]
            for tp in types:
                current_lvl = self.character.get(f"{tp}_level")
                level = current_lvl - (current_lvl % 5)
                items = CRAFT_ITEMS[tp][level]
                for chrctr in range(5):
                    for item in items:
                        await self.craft_item_scenario(item)
                        await self.drop_all()
                for item in items:
                    n = self.game.get_bank_items(item).get("quantity")
                    if n > 34:
                        await self.recycling_from_bank(item, n - 5)

    async def wait_before_action(self):
        now = datetime.utcnow()
        dt = datetime.strptime(self.character["cooldown_expiration"], "%Y-%m-%dT%H:%M:%S.%fZ")
        cd = (dt - now).total_seconds()
        print(cd)
        if cd > 0:
            await asyncio.sleep(cd)

    async def main_mode(self):  # Lert
        await self.wait_before_action()
        # await self.recycling_from_bank("greater_wooden_staff", 10)
        # await self.recycling_from_bank("fire_bow", 4)
        # await self.recycling_from_bank("iron_dagger", 5)
        # await self.recycling_from_bank("multislimes_sword", 1)
        # await self.recycling_from_bank("mushmush_bow", 4)
        # await self.recycling_from_bank("mushstaff", 2)
        await self.drop_all()
        await self.crafter()

    async def work_helper_mode0(self):  # Ralernan (miner/metallurgist)
        await self.wait_before_action()
        await self.drop_all()
        # await self.do_task()
        item_list = [
            "gold",
            "gold",
            "steel",
            "steel",
            "iron",
            "iron",
            "iron",
            "cowhide",
            "red_slimeball",
        ]
        while True:
            for i in item_list:
                await self.craft_item_scenario(i, 10)
                await self.drop_all()

    async def work_helper_mode1(self):  # Kerry
        await self.wait_before_action()
        await self.drop_all()
        # await self.do_task()
        item_list = [
            # "gold",
            # "gold",
            "steel",
            "steel",
            "iron",
            "iron",
            "iron",
            "yellow_slimeball",
        ]
        while True:
            for i in item_list:
                await self.craft_item_scenario(i, 10)
                await self.drop_all()

    async def work_helper_mode2(self):  # Karven (lamberjack/carpenter)
        await self.wait_before_action()
        await self.drop_all()
        # await self.do_task()
        item_list = [
            "dead_wood_plank",
            "dead_wood_plank",
            "spruce_plank",
            "hardwood_plank",
            "spruce_plank",
            "hardwood_plank",
            "spruce_plank",
        ]
        while True:

            for i in item_list:
                await self.craft_item_scenario(i, 10)
                await self.drop_all()

    async def work_helper_mode3(self):  # Warrant (miner/metallurgist/fisher/shef)
        await self.wait_before_action()
        await self.drop_all()
        # await self.do_task()
        item_list = [
            "coal",
            "cooked_trout",
            "mushroom_soup",
            "cooked_wolf_meat",
            "beef_stew",
            "fried_eggs",
            "cheese",
        ]
        while True:
            for i in item_list:
                await self.craft_item_scenario(i, 10)
                await self.drop_all()


if __name__ == '__main__':
    print("It's not executable file")
