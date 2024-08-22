import asyncio
from datetime import datetime
from base_api import API


def wait(func):
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        if response:
            cooldown = response.get("cooldown", {}).get("total_seconds", 0)
            await asyncio.sleep(cooldown)
        return response

    return wrapper


class BasePlayer(API):
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
            bank: list = self.game.bank.items.get(code)
            if bank:
                self.game.bank.items[code] += quantity
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
        bank: list = self.game.bank.items.get(code)
        if bank:
            await self.move(4, 1)
            if self.game.bank.items[code] <= quantity:
                response = self.post(
                    endpoint=endpoint,
                    data={"code": code,
                          "quantity": self.game.bank.items[code]}
                )
            else:
                response = self.post(
                    endpoint=endpoint,
                    data={"code": code,
                          "quantity": quantity}
                )
            character = response.get("character")

            # Decrease or remove from bank
            if self.game.bank.items[code] == quantity:
                self.game.bank.items.pop(code)
            else:
                self.game.bank.items[code] -= quantity

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


if __name__ == '__main__':
    print("It's not executable file")
