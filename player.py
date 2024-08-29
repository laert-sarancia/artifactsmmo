import time
from dataclasses import dataclass
from parameters import CRAFT_ITEMS, SLOT_TYPES, COORDINATES, ELEMENTS, CRAFTABLE
from base_player import BasePlayer


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
    def __init__(
            self,
            game,
            name: str,
            skin: str,
            level: int,
            xp: int,
            max_xp: int,
            achievements_points: int,
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
            task: str, task_type: str,
            task_progress: int,
            task_total: int,
            inventory_max_items: int,
            inventory: list[dict]):
        super().__init__(
            game,
            name,
            skin,
            level,
            xp,
            max_xp,
            achievements_points,
            gold,
            speed,
            mining_level,
            mining_xp,
            mining_max_xp,
            woodcutting_level,
            woodcutting_xp,
            woodcutting_max_xp,
            fishing_level,
            fishing_xp,
            fishing_max_xp,
            weaponcrafting_level,
            weaponcrafting_xp,
            weaponcrafting_max_xp,
            gearcrafting_level,
            gearcrafting_xp,
            gearcrafting_max_xp,
            jewelrycrafting_level,
            jewelrycrafting_xp,
            jewelrycrafting_max_xp,
            cooking_level,
            cooking_xp,
            cooking_max_xp,
            hp,
            haste,
            critical_strike,
            stamina,
            attack_fire,
            attack_earth,
            attack_water,
            attack_air,
            dmg_fire,
            dmg_earth,
            dmg_water,
            dmg_air,
            res_fire,
            res_earth,
            res_water,
            res_air,
            x,
            y,
            cooldown,
            cooldown_expiration,
            weapon_slot,
            shield_slot,
            helmet_slot,
            body_armor_slot,
            leg_armor_slot,
            boots_slot, ring1_slot,
            ring2_slot,
            amulet_slot,
            artifact1_slot,
            artifact2_slot,
            artifact3_slot,
            consumable1_slot,
            consumable1_slot_quantity,
            consumable2_slot,
            consumable2_slot_quantity, task,
            task_type,
            task_progress,
            task_total,
            inventory_max_items,
            inventory
        )

    def __repr__(self):
        return self.name

    async def take_best_tool(self, code):  # TODO check bank, inventory and level
        if self.level >= 10:
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
            if tool in self.game.bank.items:
                if self.weapon_slot != tool:
                    await self.withdraw_item(tool)
                    weapon = self.weapon_slot
                    if weapon:
                        await self.unequip("weapon")
                        await self.deposit_item(weapon)
                    await self.equip(tool, "weapon")

    async def gathering_items(self, code: str, quantity: int = 1):
        await self.take_best_tool(code)
        await self.move(*COORDINATES[code])
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
                            result = await self.craft_item_scenario(item_code, need_item)
                            if result == 500:
                                return 500
                        else:
                            result = await self.craft_item_scenario(item_code, need_item)
                            if result == 500:
                                return 500

                await self.move_to_craft(skill)
                await self.crafting(code, quantity)
            else:
                if self.game.items[code].subtype in ["woodcutting", "fishing", "mining"]:
                    if eval(f"self.{self.game.items[code].subtype}_level") > self.game.items[code].level:
                        await self.gathering_items(code, quantity)
                    else:
                        return 500
                else:
                    while self.count_inventory_item(code) < quantity:
                        monsters = self.game.get_monsters(drop=code)
                        if monsters:
                            monster = monsters[0].get("code")
                            result = await self.kill_monster(monster)
                            if result == 500:
                                return 500
                        else:
                            print(f"No monster here ({self.name})")
                            return 404

    def do_by_list(self, role: str) -> list:
        items = []
        start = self.level - self.level%5 - 5 if self.level - self.level%5 - 5 > 0 else 0
        stop = self.level - self.level%5 + 1
        for level in range(start, stop, 5):
            if self.level >= level and eval(f"self.{role}_level") >= level:
                if role == "cooking" and self.fishing_level < level:
                    break
                items += CRAFT_ITEMS[role][level]
        return items

    async def move_to_craft(self, skill):
        await self.move(*COORDINATES[skill])

    async def task_circle(self):
        await self.complete_task()
        await self.new_task()

    async def change_items(self, code: str):
        item_type = self.game.items[code].i_type
        slot = f'{self.game.items[code].i_type}_slot'
        if item_type in ["ring", "consumable"]:
            for i in range(1, 3):
                if eval(f'self.{item_type}{i}_slot') == code:
                    continue
                else:
                    slot = f'{item_type}{i}_slot'
        prev_item = eval(f"self.{slot}")
        if prev_item == code:
            return
        if not self.count_inventory_item(code):
            await self.withdraw_item(code)
        if eval(f'self.{slot}'):
            await self.wait_before_action()
            await self.unequip(slot.replace("_slot", ""))
            await self.deposit_item(prev_item)
        await self.wait_before_action()
        await self.equip(code, slot.replace("_slot", ""))

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
                        attak = effect.get("value", 0)
                        dmg += attak - attak * (monster_res[res] * 0.01)
            if best[0] < dmg and self.level >= self.game.items[weapon].level:
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

    @time_it
    async def take_best_gear(self, monster):
        monster_attack = self.game.monsters[monster].get_attack()
        monster_res = self.game.monsters[monster].get_res()

        bank_items = [item for item in self.game.bank.items]
        tekken_items = []
        for slot in SLOT_TYPES:
            if eval(f"self.{slot}"):
                tekken_items.append(eval(f"self.{slot}"))
        my_items = [item.get("code") for item in self.inventory if item.get("code")]
        all_items = my_items + bank_items + tekken_items

        for slot_type, item_type in SLOT_TYPES.items():
            if "weapon" in slot_type:
                continue
            elif "art" in slot_type:
                break
            gears = {item: self.game.items[item].effects for item in all_items if
                          self.game.items[item].i_type == item_type and
                          self.game.items[item].level <= self.level}
            if not gears:
                continue

            best: tuple[int, str | None] = (-100, None)
            for gear, stats in gears.items():
                dmg = 0
                df = 0
                for effect in stats:
                    if effect["name"] == "hp":
                        dmg += effect.get("value", 0)
                    for val in monster_attack:
                        if val in effect["name"]:
                            bonus_damage = effect.get("value", 0)
                            attak = eval(f"self.attack_{val}")
                            total_damage = attak * (1 + bonus_damage * 0.01)
                            dmg += total_damage - total_damage * (monster_res[val] * 0.01)
                            df += monster_attack[val] - monster_attack[val] * (eval(f"self.res_{val}") * 0.01)
                result_dmg = dmg - df

                if best[0] < result_dmg:
                    best = (result_dmg, gear)
            if best[1]:
                if eval(f"self.{slot_type}") != best[1]:
                    if self.count_inventory_item(best[1]):
                        await self.unequip(item_type)
                        await self.equip(best[1], item_type)
                    else:
                        await self.change_items(best[1])

    async def kill_monster(self, monster: str, quantity: int = 1):
        await self.take_best_weapon(monster)
        await self.take_best_gear(monster)
        if await self.is_win(monster):
            await self.wait_before_action()
            await self.move(**self.game.get_monster_coord(monster))
            for i in range(quantity):
                result = await self.fight()
                if result == {}:
                    return 500
        else:
            print(f"Too hard monster {monster} ({self.name})")
            return 500

    async def is_win(self, monster) -> bool:
        mob = self.game.monsters[monster]

        my_hp = self.hp
        mob_hp = mob.hp
        my_dmg = 0
        mob_dmg = 0
        for el in ELEMENTS:
            my_el_attak = eval(f"self.attack_{el}")
            mob_el_attak = eval(f"mob.attack_{el}")
            my_el_dmg = (eval(f"self.dmg_{el}"))
            mob_el_res = eval(f"mob.res_{el}")
            my_el_res = eval(f"self.res_{el}")
            my_el_full_dmg = my_el_attak * (1 + my_el_dmg * 0.01)

            my_dmg += my_el_full_dmg - my_el_full_dmg * (mob_el_res * 0.01)
            mob_dmg += mob_el_attak - mob_el_attak * (my_el_res * 0.01)

        for i in range(100):
            mob_hp -= my_dmg
            my_hp -= mob_dmg
            if mob_hp <= 0 or my_hp <= 0:
                return False if my_hp <= 0 else True

    async def do_task(self):
        if self.task_type == "monsters":
            monster = self.task
            result = await self.kill_monster(
                monster,
                self.task_total - self.task_progress)
            if result == 500:
                return 500
            else:
                await self.task_circle()

    async def drop_all(self):
        inventory = self.inventory
        if inventory:
            for slot in reversed(inventory):
                if slot["quantity"]:
                    await self.deposit_item(slot["code"], slot["quantity"])
                    await self.deposit_money(self.gold)

    async def crafter(self):
        if not self.task:
            await self.new_task()
        max_level = 0
        while True:
            await self.wear()
            await self.do_task()
            await self.drop_all()
            bank_items = self.game.bank.items.get("tasks_coin", 0)
            if bank_items:
                if bank_items > 2:
                    await self.withdraw_item("tasks_coin", bank_items // 3 * 3)
                    for _ in range(bank_items // 3):
                        await self.task_exchange()
                    await self.drop_all()
            types = {
                "gearcrafting": self.gearcrafting_level,
                "weaponcrafting": self.weaponcrafting_level,
                # "jewelrycrafting": self.jewelrycrafting_level
            }
            if len(set(types.values())) == 1:
                tp = "gearcrafting"
                level = types[tp] - (types[tp] % 5)
                items = CRAFT_ITEMS[tp][level]
                for chrctr in range(5):
                    for item in items:
                        result = await self.craft_item_scenario(item)
                        if result in [404, 500]:
                            break
                        await self.drop_all()
                for item in items:
                    n = self.game.bank.items.get(item)
                    if n > 10:
                        await self.recycling_item(item, n - 5)
            else:
                for tp in types:
                    if types[tp] >= max_level:
                        max_level = types[tp]
                        continue
                    level = types[tp] - (types[tp] % 5)
                    items = CRAFT_ITEMS[tp][level]
                    for chrctr in range(5):
                        for item in items:
                            result = await self.craft_item_scenario(item)
                            if result in [404, 500]:
                                break
                            await self.drop_all()
                    for item in items:
                        n = self.game.bank.items.get(item)
                        if n > 10:
                            await self.recycling_item(item, n - 5)

    async def recycling_item(self, code, quantity: int = 1):
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

    async def recycle_all(self):
        items = [item for item in self.game.bank.items if
                 self.game.items[item].i_type in CRAFTABLE and
                 self.game.items[item].craft]
        for item in items:
            n = self.game.bank.items.get(item)
            if n > 10:
                await self.recycling_item(item, n - 5)

    async def take_food(self):
        if self.consumable1_slot_quantity == 0 or self.consumable2_slot_quantity == 0:
            items = [item for item in self.game.bank.items if self.game.items[item].i_type == "consumable"]
            if items:
                if self.consumable1_slot == items[0] or self.consumable1_slot == items[0]:
                    return
                if self.game.bank.items[items[0]] >= 50:
                    qty = 50
                else:
                    qty = self.game.bank.items[items[0]]
                await self.withdraw_item(items[0], qty)
                slot = "consumable1" if not self.consumable1_slot_quantity else "consumable2"
                await self.equip(items[0], slot, qty)

    async def wear(self):
        for slot in SLOT_TYPES:
            if "art" in slot:
                break
            elif not eval(f"self.{slot}"):
                inventory = [item.get("code") for
                             item in self.inventory if item.get("code") and
                             self.game.items[item.get("code")].i_type == SLOT_TYPES[slot]]
                bank = [item for item in self.game.bank.items if
                        self.game.items[item].i_type == SLOT_TYPES[slot]]
                if inventory:
                    await self.equip(bank[-1], slot.replace("_slot", ""))
                elif bank:
                    await self.withdraw_item(bank[-1])
                    await self.equip(bank[-1], slot.replace("_slot", ""))
        await self.take_food()

    async def extra_action(self):
        # await self.withdraw_item("copper_ring", 10)
        # await self.sell("copper_ring", 10)

        # await self.recycling_item("wooden_shield", 7)
        # await self.recycling_item("copper_armor", 3)
        # await self.recycling_item("copper_legs_armor", 2)
        # await self.recycling_item("feather_coat", 4)
        # await self.recycling_item("copper_dagger", 1)

        # await self.withdraw_money(self.game.bank.money["gold"])
        # await self.buy("feather_coat", 25)
        # await self.craft_item_scenario("spruce_fishing_rod", 1)
        # await self.sell("fire_staff", 10)

        # await self.equip("copper_legs_armor", "leg_armor")
        # await self.recycling_item("feather_coat", 20)
        # await self.sell("feather", 40)

        await self.drop_all()

    async def main_mode(self):  # Lert
        await self.wait_before_action()
        await self.extra_action()
        await self.drop_all()
        await self.crafter()

    async def work_helper_mode0(self):  # Ralernan (miner/metallurgist)
        await self.wait_before_action()
        if not self.task:
            await self.new_task()
        await self.drop_all()
        while True:
            await self.wear()
            await self.do_task()
            await self.drop_all()
            await self.recycle_all()
            for item in self.do_by_list("jewelrycrafting"):
                result = await self.craft_item_scenario(item, 1)
                if result in [404, 500]:
                    continue
                await self.drop_all()

    async def work_helper_mode1(self):  # Kerry
        await self.wait_before_action()
        if not self.task:
            await self.new_task()
        await self.drop_all()
        while True:
            await self.wear()
            await self.do_task()
            await self.drop_all()
            for item in self.do_by_list("mining"):
                result = await self.craft_item_scenario(item, 10)
                if result in [404, 500]:
                    continue
                await self.drop_all()

    async def work_helper_mode2(self):  # Karven (lamberjack/carpenter)
        await self.wait_before_action()
        if not self.task:
            await self.new_task()
        await self.drop_all()
        while True:
            await self.wear()
            await self.do_task()
            await self.drop_all()
            for item in self.do_by_list("woodcutting"):
                result = await self.craft_item_scenario(item, 10)
                if result in [404, 500]:
                    continue
                await self.drop_all()

    async def work_helper_mode3(self):  # Warrant (miner/metallurgist/fisher/shef)
        await self.wait_before_action()
        if not self.task:
            await self.new_task()
        await self.drop_all()
        while True:
            await self.wear()
            await self.do_task()
            await self.drop_all()
            for item in self.do_by_list("cooking"):
                result = await self.craft_item_scenario(item, 10)
                if result in [404, 500]:
                    continue
                await self.drop_all()


if __name__ == '__main__':
    print("It's not executable file")
