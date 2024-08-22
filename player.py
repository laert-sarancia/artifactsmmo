import asyncio
import time
from dataclasses import dataclass
from parameters import CRAFT_ITEMS
from base_player import BasePlayer, wait


def time_it(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        lag = end_time - start_time
        if lag > 0:
            print(f"lag: {lag:.4f} {args}")
        return result

    return wrapper


@dataclass
class Player(BasePlayer):
    def __init__(self, game, name: str, skin: str, level: int, xp: int, max_xp: int, total_xp: int, gold: int,
                 speed: int, mining_level: int, mining_xp: int, mining_max_xp: int, woodcutting_level: int,
                 woodcutting_xp: int, woodcutting_max_xp: int, fishing_level: int, fishing_xp: int, fishing_max_xp: int,
                 weaponcrafting_level: int, weaponcrafting_xp: int, weaponcrafting_max_xp: int, gearcrafting_level: int,
                 gearcrafting_xp: int, gearcrafting_max_xp: int, jewelrycrafting_level: int, jewelrycrafting_xp: int,
                 jewelrycrafting_max_xp: int, cooking_level: int, cooking_xp: int, cooking_max_xp: int, hp: int,
                 haste: int, critical_strike: int, stamina: int, attack_fire: int, attack_earth: int, attack_water: int,
                 attack_air: int, dmg_fire: int, dmg_earth: int, dmg_water: int, dmg_air: int, res_fire: int,
                 res_earth: int, res_water: int, res_air: int, x: int, y: int, cooldown: int, cooldown_expiration: str,
                 weapon_slot: str, shield_slot: str, helmet_slot: str, body_armor_slot: str, leg_armor_slot: str,
                 boots_slot: str, ring1_slot: str, ring2_slot: str, amulet_slot: str, artifact1_slot: str,
                 artifact2_slot: str, artifact3_slot: str, consumable1_slot: str, consumable1_slot_quantity: int,
                 consumable2_slot: str, consumable2_slot_quantity: int, task: str, task_type: str, task_progress: int,
                 task_total: int, inventory_max_items: int, inventory: list[dict]):
        super().__init__(game, name, skin, level, xp, max_xp, total_xp, gold, speed, mining_level, mining_xp,
                         mining_max_xp, woodcutting_level, woodcutting_xp, woodcutting_max_xp, fishing_level,
                         fishing_xp, fishing_max_xp, weaponcrafting_level, weaponcrafting_xp, weaponcrafting_max_xp,
                         gearcrafting_level, gearcrafting_xp, gearcrafting_max_xp, jewelrycrafting_level,
                         jewelrycrafting_xp, jewelrycrafting_max_xp, cooking_level, cooking_xp, cooking_max_xp, hp,
                         haste, critical_strike, stamina, attack_fire, attack_earth, attack_water, attack_air, dmg_fire,
                         dmg_earth, dmg_water, dmg_air, res_fire, res_earth, res_water, res_air, x, y, cooldown,
                         cooldown_expiration, weapon_slot, shield_slot, helmet_slot, body_armor_slot, leg_armor_slot,
                         boots_slot, ring1_slot, ring2_slot, amulet_slot, artifact1_slot, artifact2_slot,
                         artifact3_slot, consumable1_slot, consumable1_slot_quantity, consumable2_slot,
                         consumable2_slot_quantity, task, task_type, task_progress, task_total, inventory_max_items,
                         inventory)
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

    async def take_best_tool(self, code):  # TODO check bank, inventory and level
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
            weapon = self.weapon_slot
            if weapon:
                await self.unequip("weapon")
                await self.deposit_item(weapon)
            await self.equip(tool, "weapon")

    async def gathering_items(self, code: str, quantity: int = 1):
        await self.take_best_tool(code)
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
                            await self.craft_item_scenario(item_code, need_item)
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
                        damage = eval(f"self.dmg_{res}")
                        dmg += effect.get("value", 0) * (damage * 0.01) - effect.get("value", 0) * (monster_res[res] * 0.01)
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
        bank = self.game.bank.items.get(code, 0)

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
            bank_items = self.game.bank.items.get("tasks_coin", 0)
            if bank_items:
                if bank_items > 2:
                    await self.withdraw_item("tasks_coin", bank_items // 3 * 3)
                    for _ in range(bank_items // 3):
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
                    n = self.game.bank.items.get(item)
                    if n > 34:
                        await self.recycling_from_bank(item, n - 5)

    async def main_mode(self):  # Lert
        await self.wait_before_action()
        await self.drop_all()
        # await self.do_task()
        await self.craft_item_scenario("forest_whip", 3)
        await self.drop_all()
        await self.craft_item_scenario("skull_staff", 3)
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
