import asyncio
from base_api import API

CRAFT_ITEMS = {
    "cooking": {
        5: ["cooked_gudgeon"],
        10: ["cooked_gudgeon"],
        15: ["cooked_shrimp"],
        20: ["cooked_shrimp"],
        25: ["cooked_trout"],
        30: ["cooked_trout"],
    },
    "weaponcrafting": {
        5: ["copper_dagger", "wooden_staff"],
        10: ["fire_staff", "sticky_dagger", "sticky_sword", "water_bow"],
        15: ["iron_dagger", "greater_wooden_staff"],
        20: ["multislimes_sword", "multislimes_sword", "multislimes_sword", "multislimes_sword", "multislimes_sword",
             "multislimes_sword", "multislimes_sword", "multislimes_sword", "multislimes_sword", "multislimes_sword",
             "mushstaff", "mushmush_bow"],
        25: ["battlestaff", "steel_axe", "skull_staff", "forest_whip", ],
        30: ["skull_wand", "dreadful_staff"],
    },
    "gearcrafting": {
        5: ["copper_boots"],
        10: ["copper_armor", "copper_legs_armor", "feather_coat"],
        15: ["iron_boots", "iron_boots", "iron_boots", "iron_helm"],
        20: ["magic_wizard_hat", "steel_helm", "steel_boots", "steel_armor"],
        25: ["magic_wizard_hat", "steel_helm", "steel_boots", "steel_armor"],
        30: ["magic_wizard_hat", "steel_helm", "steel_boots", "steel_armor"],
    },
    "jewelrycrafting": {
        5: ["copper_ring"],
        10: ["life_amulet"],
        15: ["iron_ring"],
        20: ["life_ring", "air_ring", "earth_ring", "fire_ring", "water_ring"],
        25: ["steel_ring", "steel_ring", "steel_ring", "steel_ring", "steel_ring",
             "steel_ring", "steel_ring", "steel_ring", "steel_ring", "steel_ring",
             "ring_of_chance", "dreadful_ring", "skull_ring", ],
        30: ["gold_ring", "gold_ring", "gold_ring", "gold_ring", "gold_ring",
             "gold_ring", "gold_ring", "gold_ring", "gold_ring", "gold_ring",
             "ruby_ring", "topaz_ring", "sapphire_ring", "emerald_ring"],
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


class Game(API):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.items = {item["code"]: item for item in self.get_items(page=0)}
        self.monsters = {item["code"]: item for item in self.get_monsters()}
        self.character = self.get_character()

    def __repr__(self) -> str:
        return self.name

    # ******* CHARACTER ACTIONS ****** #
    @wait
    async def move(self, x: int, y: int) -> dict | list:
        if self.character.get("x") != x or self.character.get("y") != y:
            response = self.post(
                endpoint=f"/my/{self.name}/action/move",
                data={"x": x, "y": y}
            )
            self.character = response.get("character")
            return response

    @wait
    async def gathering(self) -> dict | list:
        response = self.post(f"/my/{self.name}/action/gathering")
        if response:
            self.character = response.get("character")
        return response

    @wait
    async def crafting(self, code: str, quantity: int = 1) -> dict | list:
        response = self.post(
            endpoint=f"/my/{self.name}/action/crafting",
            data={"code": code, "quantity": quantity}
        )
        self.character = response.get("character")
        return response

    @wait
    async def equip(self, code: str, slot: str) -> dict | list:
        if self.character.get(f"{slot}_slot"):
            await self.unequip(slot)
        response = self.post(
            endpoint=f"/my/{self.name}/action/equip",
            data={"code": code, "slot": slot}
        )
        self.character = response.get("character")
        return response

    @wait
    async def unequip(self, slot: str) -> dict | list:
        response = self.post(
            endpoint=f"/my/{self.name}/action/unequip",
            data={"slot": slot}
        )
        self.character = response.get("character")
        return response

    @wait
    async def sell(self, code: str, quantity: int = 1) -> dict | list:
        await self.move(5, 1)
        price = self.get_item(code).get("ge").get("sell_price")
        response = self.post(
            endpoint=f"/my/{self.name}/action/ge/sell",
            data={"code": code,
                  "quantity": quantity,
                  "price": price}
        )
        self.character = response.get("character")
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
            self.character = response.get("character")
            return response

    @wait
    async def withdraw_item(self, code: str, quantity: int = 1) -> dict | list:
        endpoint = f"/my/{self.name}/action/bank/withdraw"
        bank = [it for it in self.get_bank_items(code) if it.get("code") == code]
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
            self.character = response.get("character")
            return response
        else:
            print(f"No items {code} ({self.name})")

    @wait
    async def recycling(self, code: str, quantity: int = 1) -> dict | list:
        response = self.post(
            endpoint=f"/my/{self.name}/action/recycling",
            data={
                "code": code,
                "quantity": quantity
            }
        )
        return response

    @wait
    async def fight(self) -> dict | list:
        response = self.post(endpoint=f"/my/{self.name}/action/fight")
        self.character = response.get("character")
        fight_result = response.get("fight")
        if fight_result.get("result") == "lose":
            print(f"Monster too strong for {self.name}")
        elif fight_result.get("drops"):
            drops = [f'{item["quantity"]} {item["code"]}' for item in fight_result.get("drops")]
            print(f'Won {", ".join(drops)} ({self.name})')
        return response

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

    # ******* GAME ACTIONS ****** #

    def get_bank_items(self, code: str | None = None) -> dict | list:
        endpoint = "/my/bank/items"
        if code:
            response = self.get(
                endpoint=endpoint,
                params={"item_code": code})
        else:
            response = self.get(endpoint)
        return response

    def get_monster(self, code: str) -> dict:
        """
        Deprecated
        :param code:
        :return: dictionary with monster info
        """
        response = self.get(endpoint=f"/monsters/{code}")
        return response

    def get_monsters(self, drop: str | None = None) -> dict | list:
        response = self.get(
            endpoint="/monsters/",
            params={"drop": drop})
        return response

    async def get_resources(self) -> dict | list:
        response = self.get(endpoint="/resources/")
        return response

    def get_item(self, code: str) -> dict | list:
        response = self.get(endpoint=f"/items/{code}")
        data = response
        if data:
            return data
        else:
            print(f"Incorrect code {code} ({self.name})")

    def get_items(
            self,
            craft_skill=None,
            max_level: int = 30,
            min_lvl: int = 0,
            item_type=None,
            page: int = 1
    ) -> dict | list:
        endpoint = "/items/"
        params = {}
        if craft_skill:
            params.update({"craft_skill": craft_skill})
        if max_level:
            params.update({"max_level": max_level})
        if min_lvl:
            params.update({"min_lvl": min_lvl})
        if item_type:
            params.update({"item_type": item_type})
        if page:
            params.update({"craft_skill": page})
        result = []
        if params:
            if page != 0:
                response = self.get(
                    endpoint=endpoint,
                    params=params
                )
                return response
            else:
                for page in range(1, 5):
                    result += self.get(
                        endpoint=endpoint,
                        params={**params,
                                "page": page}
                    )
            return result
        else:
            response = self.get(
                endpoint=endpoint
            )
            return response

    def get_exchange_items(self) -> dict | list:
        response = self.get(endpoint="/ge/")
        return response

    def get_maps(self, content: str) -> dict | list:
        response = self.get(
            endpoint="/maps/",
            params={"content_code": content})
        return response

    def get_map(self, x: int, y: int) -> dict | list:
        response = self.get(endpoint=f"/maps/{x}/{y}")
        return response

    def get_monster_coord(self, name: str) -> dict | list:
        monsters = self.get_maps(name)
        return {"x": monsters[0].get("x"), "y": monsters[0].get("y")}

    # ******* COMPLEX ACTIONS ****** #

    async def gathering_items(self, code: str, quantity: int = 1):
        weapon = self.character.get("weapon_slot")
        subtype = self.items[code].get("subtype")
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
            craft = self.items[code].get("craft")
            if craft:
                skill, level, components, qty = craft.values()
                for item in components:
                    item_code = item.get("code")
                    item_quantity = item.get("quantity")
                    bank = [it for it in self.get_bank_items(item_code) if it.get("code") == item_code]
                    if bank:
                        if bank[0].get("quantity") > item_quantity * quantity:
                            await self.withdraw_item(item_code, item_quantity * quantity)
                        else:
                            await self.withdraw_item(item_code, bank[0].get("quantity"))
                    if self.count_inventory_item(item_code) < item_quantity * quantity:
                        await self.craft_item_scenario(
                            item_code,
                            item_quantity * quantity - self.count_inventory_item("code"))
                await self.move_to_craft(skill)
                await self.crafting(code, quantity)
            else:
                if self.items[code].get("subtype") in ["woodcutting", "fishing", "mining"]:
                    await self.gathering_items(code, quantity)
                else:
                    while self.count_inventory_item(code) < quantity:
                        monsters = self.get_monsters(drop=code)
                        if monsters:
                            monster = monsters[0].get("code")
                            await self.kill_monster(monster)
                        else:
                            print(f"No monster here ({self.name})")
                            return

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
        await self.task_exchange()

    async def change_items(self, code: str):
        i_type = self.items[code].get("type")
        slot = f'{i_type}_slot'
        if i_type == "ring":
            slot = f'{i_type}1_slot'  # TODO check 2nd ring
        current_item = self.character.get(slot)
        bank_items = [item.get("code") for item in self.get_bank_items()]
        my_items = [item.get("code") for item in self.character.get("inventory") if item.get("code")]
        all_items = my_items + bank_items
        if code in all_items:
            if not self.count_inventory_item(code):
                await self.withdraw_item(code)
        await self.equip(code, slot)
        await self.deposit_item(current_item)

    async def kill_monster(self, monster: str, quantity: int = 1):
        monster_stats = self.monsters[monster]
        monster_res = {key: value for key, value in monster_stats.items() if "res_" in key}
        min_res: str = min(monster_res, key=monster_res.get)
        el = min_res.replace("res_", "attack_")
        bank_items = [item.get("code") for item in self.get_bank_items()]
        my_items = [item.get("code") for item in self.character.get("inventory") if item.get("code")]
        all_items = my_items + bank_items
        weapons = {}
        for weapon in all_items:
            item = self.items[weapon]
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

        await self.move(**self.get_monster_coord(monster))
        for i in range(quantity):
            await self.fight()

    async def do_task(self):
        if self.character.get("task_type") == "monsters":
            await self.kill_monster(
                self.character.get("task"),
                self.character.get("task_total") - self.character.get("task_progress"))
        await self.task_circle()

    async def drop_all(self):
        inventory = self.character.get("inventory")
        for slot in reversed(inventory):
            if slot["quantity"]:
                await self.deposit_item(slot["code"], slot["quantity"])

    async def recycling_from_bank(self, code, quantity: int = 1):
        await self.withdraw_item(code, quantity)
        await self.move_to_craft(self.items[code].get("craft").get("skill"))
        await self.recycling(code, quantity)
        await self.drop_all()

    async def rise_cook_level_5(self, quantity: int = 1):
        while self.character.get("fishing_level") < 5:
            await self.craft_item_scenario("cooked_gudgeon", quantity)
            await self.drop_all()

    async def rise_cook_level_10(self, quantity: int = 1):
        while self.character.get("weaponcrafting_level") < 10:
            await self.craft_item_scenario("cooked_gudgeon", quantity)
            await self.drop_all()

    async def rise_jewel_level_5(self, quantity: int = 1):
        while self.character.get("jewelrycrafting_level") < 5:
            await self.craft_item_scenario("copper_ring", quantity)
            await self.drop_all()

    async def rise_jewel_level_10(self, quantity: int = 1):
        while self.character.get("jewelrycrafting_level") < 10:
            await self.craft_item_scenario("life_amulet", quantity)
            await self.drop_all()

    async def rise_jewel_level_15(self, quantity: int = 1):
        while self.character.get("jewelrycrafting_level") < 15:
            await self.craft_item_scenario("iron_ring", quantity)
            await self.drop_all()

    async def rise_gear_level_5(self, quantity: int = 1):
        while self.character.get("gearcrafting_level") < 5:
            await self.craft_item_scenario("copper_boots", quantity)
            await self.drop_all()

    async def rise_gear_level_10(self, quantity: int = 1):
        item_list = [
            "copper_armor",
            "copper_legs_armor",
            "feather_coat",
        ]
        while self.character.get("gearcrafting_level") < 10:
            for it in item_list:
                await self.craft_item_scenario(it, quantity)
            await self.drop_all()

    async def rise_gear_level_15(self, quantity: int = 1):
        item_list = [
            "iron_boots",
            "iron_boots",
            "iron_boots",
            "iron_helm",
        ]
        while self.character.get("gearcrafting_level") < 15:
            for it in item_list:
                await self.craft_item_scenario(it, quantity)
                await self.drop_all()

    async def rise_weapon_level_5(self, quantity: int = 1):
        item_list = [
            "copper_dagger",
            "wooden_staff",
        ]
        while self.character.get("weaponcrafting_level") < 5:
            for it in item_list:
                await self.craft_item_scenario(it, quantity)
                await self.drop_all()

    async def rise_weapon_level_10(self, quantity: int = 1):
        item_list = [
            "fire_staff",
            "sticky_dagger",
            "sticky_sword",
            "water_bow",
        ]
        while self.character.get("weaponcrafting_level") < 10:
            for it in item_list:
                await self.craft_item_scenario(it, quantity)
                await self.drop_all()

    async def rise_weapon_level_15(self, quantity: int = 1):
        item_list = [
            "iron_dagger",
            "greater_wooden_staff",
        ]
        while self.character.get("weaponcrafting_level") < 15:
            for it in item_list:
                await self.craft_item_scenario(it, quantity)
                await self.drop_all()

    async def rise_weapon_level_20(self, quantity: int = 1):
        item_list = [
            "multislimes_sword",
            "multislimes_sword",
            "multislimes_sword",
            "multislimes_sword",
            "multislimes_sword",
            "multislimes_sword",
            "multislimes_sword",
            "multislimes_sword",
            "multislimes_sword",
            "multislimes_sword",
            "mushstaff",
            "mushmush_bow",
        ]
        while self.character.get("weaponcrafting_level") < 20:
            for it in item_list:
                await self.craft_item_scenario(it, quantity)
                await self.drop_all()

    async def level_5(self):
        await self.unequip("weapon")
        await self.craft_item_scenario("wooden_staff", 3)
        await self.equip("wooden_staff", "weapon")
        await self.drop_all()

        await self.craft_item_scenario("copper_boots", 3)
        await self.equip("copper_boots", "boots")
        await self.drop_all()

        await self.craft_item_scenario("wooden_shield", 5)
        await self.equip("wooden_shield", "shield")
        await self.drop_all()

        await self.craft_item_scenario("copper_helmet", 5)
        await self.equip("copper_helmet", "helmet")
        await self.drop_all()

        await self.craft_item_scenario("copper_ring", 10)
        await self.equip("copper_ring", "ring1")
        await self.equip("copper_ring", "ring2")
        await self.drop_all()

        await self.rise_weapon_level_5()

        await self.rise_gear_level_5()
        await self.craft_item_scenario("copper_legs_armor", 5)
        await self.equip("copper_legs_armor", "leg_armor")
        await self.drop_all()

        await self.craft_item_scenario("copper_armor", 3)
        await self.equip("copper_armor", "body_armor")
        await self.drop_all()
        await self.craft_item_scenario("feather_coat", 2)
        await self.equip("feather_coat", "body_armor")
        await self.drop_all()

        await self.rise_jewel_level_5()
        await self.craft_item_scenario("life_amulet", 5)
        await self.equip("life_amulet", "amulet")
        await self.drop_all()

        await self.do_task()

    async def level_10(self):
        await self.rise_weapon_level_10()
        await self.craft_item_scenario("iron_sword", 5)
        await self.equip("iron_sword", "weapon")
        await self.sell("wooden_staff")
        await self.deposit_item("iron_sword", 4)

        await self.unequip("weapon")
        await self.craft_item_scenario("iron_dagger", 5)
        await self.deposit_item("iron_dagger", 4)

        await self.unequip("weapon")
        await self.craft_item_scenario("fire_bow", 5)
        await self.deposit_item("fire_bow", 4)

        await self.unequip("weapon")
        await self.craft_item_scenario("greater_wooden_staff", 5)
        await self.deposit_item("greater_wooden_staff", 4)

        await self.rise_gear_level_10()
        await self.craft_item_scenario("iron_boots", 3)
        await self.equip("iron_boots", "boots")
        await self.sell("copper_boots")
        await self.deposit_item("iron_boots", 2)

        await self.craft_item_scenario("slime_shield", 5)
        await self.equip("slime_shield", "shield")
        await self.sell("wooden_shield")
        await self.deposit_item("slime_shield", 4)

        await self.craft_item_scenario("iron_legs_armor", 5)
        await self.equip("iron_legs_armor", "leg_armor")
        await self.sell("copper_legs_armor")
        await self.deposit_item("iron_legs_armor", 4)

        await self.craft_item_scenario("adventurer_vest", 5)
        await self.equip("adventurer_vest", "body_armor")
        await self.sell("copper_armor")
        await self.deposit_item("adventurer_vest", 4)

        await self.craft_item_scenario("adventurer_helmet", 5)
        await self.equip("adventurer_helmet", "helmet")
        await self.sell("copper_helmet")
        await self.deposit_item("adventurer_helmet", 4)

        await self.rise_jewel_level_10()
        await self.craft_item_scenario("iron_ring", 10)
        await self.equip("iron_ring", "ring1")
        await self.equip("iron_ring", "ring2")
        await self.sell("copper_ring", 2)
        await self.deposit_item("iron_ring", 8)

        await self.craft_item_scenario("life_amulet", 5)
        await self.equip("life_amulet", "amulet")
        await self.deposit_item("life_amulet", 4)

        await self.craft_item_scenario("fire_and_earth_amulet", 3)
        await self.equip("fire_and_earth_amulet", "amulet")
        await self.sell("life_amulet")
        await self.deposit_item("fire_and_earth_amulet", 2)
        await self.craft_item_scenario("air_and_water_amulet", 2)
        await self.deposit_item("air_and_water_amulet", 2)

        await self.do_task()

    async def crafter(self):
        await self.new_task()
        while True:
            for level in range(0, 30, 5):
                types = ["cooking",
                         "weaponcrafting",
                         "gearcrafting",
                         "jewelrycrafting"]
                for tp in types:
                    items = self.get_items(min_lvl=level, max_level=level, item_type=tp)
                    for chrctr in range(5):
                        for item in items:
                            await self.craft_item_scenario(item)
                            await self.drop_all()
                    for item in items:
                        n = self.get_bank_items(item).get("quantity")
                        if n > 34:
                            await self.recycling_from_bank(item, n - 5)

    async def main_mode(self):  # Lert
        # await self.drop_all()
        await self.do_task()
        await self.rise_weapon_level_20(2)

    async def work_helper_mode0(self):  # Ralernan (miner/metallurgist)
        # await self.drop_all()
        await self.do_task()
        item_list = [
            "iron",
            "iron",
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
        # await self.drop_all()
        await self.do_task()
        item_list = [
            "iron",
            "iron",
            "iron",
            "iron",
            "iron",
            "red_slimeball",
        ]
        while True:
            for i in item_list:
                await self.craft_item_scenario(i, 10)
                await self.drop_all()

    async def work_helper_mode2(self):  # Karven (lamberjack/carpenter)
        # await self.drop_all()
        await self.do_task()
        item_list = [
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
        # await self.drop_all()
        await self.do_task()
        item_list = [
            "coal",
            "coal",
            "coal",
            "coal",
            "steel",
            "cooked_shrimp",
            "beef_stew",
        ]
        while True:
            for i in item_list:
                await self.craft_item_scenario(i, 10)
                await self.drop_all()


async def main():
    lert = Game(name="Lert")
    ralernan = Game(name="Ralernan")
    kerry = Game(name="Kerry")
    karven = Game(name="Karven")
    warrant = Game(name="Warrant")
    await asyncio.gather(
        lert.main_mode(),
        ralernan.work_helper_mode0(),
        kerry.work_helper_mode1(),
        karven.work_helper_mode2(),
        warrant.work_helper_mode3(),
    )


if __name__ == '__main__':
    asyncio.run(main())
