import asyncio
import time
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
        15: ["mushstaff", "mushstaff", "mushstaff", "mushmush_bow", "multislimes_sword"],
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


def time_it(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        lag = end_time - start_time
        if lag:
            print(f"lag: {lag:.2f} {args}")
        return result

    return wrapper


def wait(func):
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        if response:
            cooldown = response.get("cooldown", {}).get("total_seconds", 0)
            await asyncio.sleep(cooldown)
        return response

    return wrapper


class Player(API):
    def __init__(
            self,
            game,
            name: str,
            skin: str,
            level: int,
            xp: int,
            max_xp: int,
            total_xp: int,
            gold: int,
            speed: int,
            mining_level: int,
            mining_xp: int,
            mining_max_xp: int,
            woodcutting_level: int,
            woodcutting_xp: int,
            woodcutting_max_xp: int,
            fishing_level: int,
            fishing_xp: int,
            fishing_max_xp: int,
            weaponcrafting_level: int,
            weaponcrafting_xp: int,
            weaponcrafting_max_xp: int,
            gearcrafting_level: int,
            gearcrafting_xp: int,
            gearcrafting_max_xp: int,
            jewelrycrafting_level: int,
            jewelrycrafting_xp: int,
            jewelrycrafting_max_xp: int,
            cooking_level: int,
            cooking_xp: int,
            cooking_max_xp: int,
            hp: int,
            haste: int,
            critical_strike: int,
            stamina: int,
            attack_fire: int,
            attack_earth: int,
            attack_water: int,
            attack_air: int,
            dmg_fire: int,
            dmg_earth: int,
            dmg_water: int,
            dmg_air: int,
            res_fire: int,
            res_earth: int,
            res_water: int,
            res_air: int,
            x: int,
            y: int,
            cooldown: int,
            cooldown_expiration: str,
            weapon_slot: str,
            shield_slot: str,
            helmet_slot: str,
            body_armor_slot: str,
            leg_armor_slot: str,
            boots_slot: str,
            ring1_slot: str,
            ring2_slot: str,
            amulet_slot: str,
            artifact1_slot: str,
            artifact2_slot: str,
            artifact3_slot: str,
            consumable1_slot: str,
            consumable1_slot_quantity: int,
            consumable2_slot: str,
            consumable2_slot_quantity: int,
            task: str,
            task_type: str,
            task_progress: int,
            task_total: int,
            inventory_max_items: int,
            inventory: list[dict]
    ):
        self.game = game
        self.name = name
        self.skin = skin
        self.level = level
        self.xp = xp
        self.max_xp = max_xp
        self.total_xp = total_xp
        self.gold = gold
        self.speed = speed
        self.mining_level = mining_level
        self.mining_xp = mining_xp
        self.mining_max_xp = mining_max_xp
        self.woodcutting_level = woodcutting_level
        self.woodcutting_xp = woodcutting_xp
        self.woodcutting_max_xp = woodcutting_max_xp
        self.fishing_level = fishing_level
        self.fishing_xp = fishing_xp
        self.fishing_max_xp = fishing_max_xp
        self.weaponcrafting_level = weaponcrafting_level
        self.weaponcrafting_xp = weaponcrafting_xp
        self.weaponcrafting_max_xp = weaponcrafting_max_xp
        self.gearcrafting_level = gearcrafting_level
        self.gearcrafting_xp = gearcrafting_xp
        self.gearcrafting_max_xp = gearcrafting_max_xp
        self.jewelrycrafting_level = jewelrycrafting_level
        self.jewelrycrafting_xp = jewelrycrafting_xp
        self.jewelrycrafting_max_xp = jewelrycrafting_max_xp
        self.cooking_level = cooking_level
        self.cooking_xp = cooking_xp
        self.cooking_max_xp = cooking_max_xp
        self.hp = hp
        self.haste = haste
        self.critical_strike = critical_strike
        self.stamina = stamina
        self.attack_fire = attack_fire
        self.attack_earth = attack_earth
        self.attack_water = attack_water
        self.attack_air = attack_air
        self.dmg_fire = dmg_fire
        self.dmg_earth = dmg_earth
        self.dmg_water = dmg_water
        self.dmg_air = dmg_air
        self.res_fire = res_fire
        self.res_earth = res_earth
        self.res_water = res_water
        self.res_air = res_air
        self.x = x
        self.y = y
        self.cooldown = cooldown
        self.cooldown_expiration = cooldown_expiration
        self.weapon_slot = weapon_slot
        self.shield_slot = shield_slot
        self.helmet_slot = helmet_slot
        self.body_armor_slot = body_armor_slot
        self.leg_armor_slot = leg_armor_slot
        self.boots_slot = boots_slot
        self.ring1_slot = ring1_slot
        self.ring2_slot = ring2_slot
        self.amulet_slot = amulet_slot
        self.artifact1_slot = artifact1_slot
        self.artifact2_slot = artifact2_slot
        self.artifact3_slot = artifact3_slot
        self.consumable1_slot = consumable1_slot
        self.consumable1_slot_quantity = consumable1_slot_quantity
        self.consumable2_slot = consumable2_slot
        self.consumable2_slot_quantity = consumable2_slot_quantity
        self.task = task
        self.task_type = task_type
        self.task_progress = task_progress
        self.task_total = task_total
        self.inventory_max_items = inventory_max_items
        self.inventory = inventory

    def __repr__(self) -> str:
        return self.name

    def get_slots(self) -> dict:
        return {
            "weapon_slot": self.weapon_slot,
            "shield_slot": self.shield_slot,
            "helmet_slot": self.helmet_slot,
            "body_armor_slot": self.body_armor_slot,
            "leg_armor_slot": self.leg_armor_slot,
            "boots_slot": self.boots_slot,
            "ring1_slot": self.ring1_slot,
            "ring2_slot": self.ring2_slot,
            "amulet_slot": self.amulet_slot,
            "artifact1_slot": self.artifact1_slot,
            "artifact2_slot": self.artifact2_slot,
            "artifact3_slot": self.artifact3_slot,
        }

    def update_character(self, **kwargs):
        self.__dict__.update(**kwargs)

    # ******* BASIC ACTIONS ****** #

    async def wait_before_action(self):
        now = datetime.strptime(self.game.get_status().get("server_time"), "%Y-%m-%dT%H:%M:%S.%fZ")
        dt = datetime.strptime(self.cooldown_expiration, "%Y-%m-%dT%H:%M:%S.%fZ")
        cd = (dt - now).total_seconds()
        if cd > 0:
            print(f"Waiting {cd:.2f} sec for {self.name}")
            await asyncio.sleep(cd)

    @wait
    async def move(self, x: int, y: int) -> dict | list:
        if self.x != x or self.y != y:
            response = self.post(
                endpoint=f"/my/{self.name}/action/move",
                data={"x": x, "y": y}
            )
            character = response.get("character")
            if character:
                self.update_character(**character)
            else:
                print(f"NO CHARACTER IN RESPONSE ({self.name})")
            return response

    @wait
    async def gathering(self) -> dict | list:
        response = self.post(f"/my/{self.name}/action/gathering")
        if response:
            character = response.get("character")
            if character:
                self.update_character(**character)
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
            self.update_character(**character)
        else:
            print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def equip(self, code: str, slot: str) -> dict | list:
        response = self.post(
            endpoint=f"/my/{self.name}/action/equip",
            data={"code": code, "slot": slot}
        )
        character = response.get("character")
        if character:
            self.update_character(**character)
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
            self.update_character(**character)
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
            self.update_character(**character)
        else:
            print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def deposit_item(self, code: str, quantity: int = 1) -> dict | list:
        endpoint = f"/my/{self.name}/action/bank/deposit"
        await self.move(4, 1)
        if self.count_inventory_item(code):
            if self.count_inventory_item(code) < quantity:
                quantity = self.count_inventory_item(code)
            response = self.post(
                endpoint=endpoint,
                data={"code": code,
                      "quantity": quantity}
            )
            character = response.get("character")

            # Increase or add to bank
            bank: list = self.game.get_bank_items(code)
            if bank:
                item = bank[0]
                item["quantity"] += quantity
            else:
                self.game.bank.items.update({code: quantity})

            if character:
                self.update_character(**character)
            else:
                print(f"NO CHARACTER IN RESPONSE ({self.name})")
            return response

    @wait
    async def withdraw_item(self, code: str, quantity: int = 1) -> dict | list:
        endpoint = f"/my/{self.name}/action/bank/withdraw"
        bank: list = self.game.get_bank_items(code)
        if bank:
            item = bank[0]
            await self.move(4, 1)
            if item["quantity"] <= quantity:
                response = self.post(
                    endpoint=endpoint,
                    data={"code": code,
                          "quantity": item.get("quantity")}
                )
            else:
                response = self.post(
                    endpoint=endpoint,
                    data={"code": code,
                          "quantity": quantity}
                )
            character = response.get("character")

            # Decrease or remove from bank
            if item["quantity"] == quantity:
                self.game.bank.items.popitem(code)
            else:
                item["quantity"] = item["quantity"] - quantity

            if character:
                self.update_character(**character)
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
            self.update_character(**character)
        else:
            print(f"NO CHARACTER IN RESPONSE ({self.name})")
        return response

    @wait
    async def fight(self) -> dict | list:
        response = self.post(endpoint=f"/my/{self.name}/action/fight")
        if response:
            character = response.get("character")
            if character:
                self.update_character(**character)
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
                    self.update_character(**character)
                else:
                    print(f"NO CHARACTER IN RESPONSE ({self.name})")
                return response

    def get_character(self) -> dict | list:
        response = self.get(endpoint=f"/characters/{self.name}")
        return response

    def get_slot_of_equip(self, code: str) -> str:
        equip: list = [slot for slot in self.get_slots() if self.get_slots()[slot] == code]
        if equip:
            return equip[0].rstrip("_slot")
        else:
            print(f"No equip {code} on {self.name}")

    def get_slot_of_item(self, code: str) -> str:
        inventory = self.inventory
        slot = [slot["slot"] for slot in inventory if slot["code"] == code]
        return slot[0]

    def check_item_on(self, code: str) -> bool:
        inventory = self.inventory
        if [slot for slot in inventory if slot["code"] == code]:
            return True
        return False

    def count_inventory_item(self, code: str) -> int:
        if self.check_item_on(code):
            qty = [slot["quantity"] for slot in self.inventory if slot["code"] == code]
            if qty:
                return sum(qty)
        else:
            return 0

    # ******* COMPLEX ACTIONS ****** #

    async def gathering_items(self, code: str, quantity: int = 1):
        weapon = self.weapon_slot
        subtype = self.game.items[code].subtype
        if subtype == "mining":
            tool = "iron_pickaxe"
        elif subtype == "woodcutting":
            tool = "iron_axe"
        elif subtype == "fishing":
            tool = "spruce_fishing_rod"
        else:
            tool = None
            print(f"Incorrect subtype {subtype} ({self.name})")
        if self.weapon_slot != tool:
            await self.withdraw_item(tool)
            if self.weapon_slot:
                await self.unequip("weapon")
            if self.count_inventory_item(code):
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
            craft = self.game.items[code].craft
            if craft:
                skill, level, components, qty = craft.values()
                for item in components:
                    item_code = item.get("code")
                    item_quantity = item.get("quantity")
                    my_item = self.count_inventory_item(item_code)
                    if my_item < item_quantity * quantity:
                        need_item = item_quantity * quantity - my_item
                        bank_item = self.game.bank.items.get(item_code, 0)
                        if bank_item > need_item:
                            await self.withdraw_item(item_code, need_item)
                        elif bank_item:
                            await self.withdraw_item(item_code, bank_item)
                            await self.craft_item_scenario(item_code, need_item - bank_item)
                        else:
                            await self.craft_item_scenario(item_code, need_item)

                await self.move_to_craft(skill)
                await self.crafting(code, quantity)
            else:
                if self.game.items[code].subtype in ["woodcutting", "fishing", "mining"]:
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
        slot = f'{self.game.items[code].i_type}'
        prev_item = eval(f"self.{slot}_slot")
        await self.withdraw_item(code)
        if eval(f'self.{slot}_slot'):
            await self.wait_before_action()
            await self.unequip(slot)
            await self.deposit_item(prev_item)
        await self.wait_before_action()
        await self.equip(code, slot)

    @time_it
    async def take_best_weapon(self, monster):
        monster_res = self.game.monsters[monster].get_res()
        bank_items = [item for item in self.game.bank.items]
        my_items = [item.get("code") for item in self.inventory if item.get("code")]
        all_items = my_items + bank_items
        weapons = {}
        for weapon in all_items:
            item = self.game.items[weapon]
            if item.i_type == "weapon" \
                    and item.level <= self.level:
                weapons[weapon] = item.effects
        best: tuple[int, str | None] = (0, None)

        for weapon, stats in weapons.items():
            dmg = 0
            for effect in stats:
                for res in monster_res:
                    if effect.get("name", None) == f"attack_{res}":
                        dmg += effect.get("value", 0) - effect.get("value", 0) * (monster_res[res] * 0.01)
            if best[0] < dmg:
                best = (dmg, weapon)
        # TODO Check all slots and change to better item!
        if best[1]:
            item_type = self.game.items[best[1]].i_type
            if eval(f"self.{item_type}_slot") != best[1]:
                if self.count_inventory_item(best[1]):
                    await self.unequip(item_type)
                    await self.equip(best[1], item_type)
                else:
                    await self.change_items(best[1])

    async def kill_monster(self, monster: str, quantity: int = 1):  # TODO calc battle and select equip
        await self.take_best_weapon(monster)
        await self.wait_before_action()
        await self.move(**self.game.get_monster_coord(monster))
        for i in range(quantity):
            result = await self.fight()
            if result == {}:
                return 500

    async def do_task(self):
        if self.task_type == "monsters":
            monster = self.task
            if self.game.monsters[monster].level < self.level:
                result = await self.kill_monster(
                    monster,
                    self.task_total - self.task_progress)
                if result == 500:
                    return 500
                await self.task_circle()
            else:
                print(f"Too hard Task {monster} ({self.name})")

    async def drop_all(self):
        inventory = self.inventory
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

        await self.move_to_craft(self.game.items[code].craft.get("skill"))
        await self.recycling(code, quantity)
        await self.drop_all()

    async def crafter(self):
        if not self.task:
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
            types = ["gearcrafting",
                     "weaponcrafting",
                     "jewelrycrafting"]
            for tp in types:
                current_lvl = eval(f"self.{tp}_level")
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

    async def main_mode(self):  # Lert
        await self.wait_before_action()
        await self.drop_all()
        await self.do_task()
        await self.craft_item_scenario("mushmush_jacket", 5)
        await self.change_items("mushmush_jacket")
        await self.drop_all()
        await self.craft_item_scenario("adventurer_boots", 5)
        await self.change_items("adventurer_boots")
        await self.drop_all()
        await self.craft_item_scenario("mushmush_wizard_hat", 3)
        await self.change_items("mushmush_wizard_hat")
        await self.drop_all()
        await self.craft_item_scenario("lucky_wizard_hat", 3)
        await self.drop_all()
        await self.craft_item_scenario("forest_whip", 3)
        await self.drop_all()
        await self.craft_item_scenario("skull_staff", 3)
        await self.drop_all()
        await self.drop_all()
        await self.crafter()

    async def work_helper_mode0(self):  # Ralernan (miner/metallurgist)
        await self.wait_before_action()
        await self.drop_all()
        await self.do_task()
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
        await self.do_task()
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
        await self.do_task()
        item_list = [
            "mushroom",
            "mushroom",
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
            "cooked_wolf_meat",
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
