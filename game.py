from dataclasses import dataclass
from parameters import SLOT_TYPES
from player import Player
from monster import Monster
from item import Item
from async_api import AsyncRequester
from exchange_view import Exchange


@dataclass
class Bank(AsyncRequester):
    async def __init__(self):
        details = await self.get_bank_details()
        self.money = details["gold"]
        self.slots = details["slots"]
        self.expansions = details["expansions"]
        self.next_expansion_cost = details["next_expansion_cost"]
        items = await self.get_bank_items(page=0)
        self.items: dict[str: int] = {item["code"]: item["quantity"] for item in items}

    def update_bank(self, **kwargs):
        self.__dict__.update(**kwargs)

    async def get_bank_details(self) -> dict | list:
        response = await self.get(endpoint="/my/bank")
        return response

    async def get_bank_items(
            self,
            code: str= "",
            page: int = 1
    ) -> dict | list:
        endpoint = "/my/bank/items"
        params = {"item_code": code}
        if code:
            params.update({"code": code})
        if page:
            params.update({"page": page})

        if page != 0:
            result = await self.get(
                endpoint=endpoint,
                params=params
            )
        else:
            result = []
            for page in range(1, 5):
                result += await self.get(
                    endpoint=endpoint,
                    params={"page": page}
                )
        return result


@dataclass
class Game(AsyncRequester):
    async def __init__(self):
        await super().__init__()
        self.items: dict[str: Item] = {item["code"]: Item(**item) for item in await self.get_items(page=0)}
        self.monsters: dict[str, Monster] = {mon["code"]: Monster(**mon) for mon in await self.get_monsters()}
        self.bank = await Bank()
        self.exchange = await Exchange(self)
        # self.players = [Player(game=self, **await self.get_character(name=player)) for player in NAMES]
        self.lert = await Player(game=self, **await self.get_character(name="Lert"))
        self.ralernan = await Player(game=self, **await self.get_character(name="Ralernan"))
        self.kerry = await Player(game=self, **await self.get_character(name="Kerry"))
        self.karven = await Player(game=self, **await self.get_character(name="Karven"))
        self.warrant = await Player(game=self, **await self.get_character(name="Warrant"))
        self.players = [self.lert, self.ralernan, self.kerry, self.karven, self.warrant]

    # ******* GAME ACTIONS ****** #

    async def update_bank(self):
        self.bank.update_bank(**await self.bank.get_bank_details())

    async def get_status(self):
        response = await self.get("/")
        return response

    async def get_character(self, name) -> dict | list:
        response = await self.get(endpoint=f"/characters/{name}")
        return response

    async def get_bank_items(
            self,
            code: str= "",
            page: int = 1
    ) -> dict | list:
        endpoint = "/my/bank/items"
        params = {"item_code": code}
        if code:
            params.update({"code": code})
        if page:
            params.update({"page": page})

        if page != 0:
            result = await self.get(
                endpoint=endpoint,
                params=params
            )
        else:
            result = []
            for page in range(1, 5):
                result += await self.get(
                    endpoint=endpoint,
                    params={**params,
                            "page": page}
                )
        return result

    # async def get_bank_details(self) -> dict | list:
    #     response = await self.get(endpoint="/my/bank")
    #     return response

    async def get_monster(self, code: str) -> dict:
        """
        Deprecated
        :param code:
        :return: dictionary with monster info
        """
        response = await self.get(endpoint=f"/monsters/{code}")
        return response

    async def get_monsters(self, drop: str = "") -> dict | list:
        if drop:
            response = await self.get(
                endpoint="/monsters/",
                params={"drop": drop})
        else:
            response = await self.get(endpoint="/monsters/")
        return response

    async def get_resources(self) -> dict | list:
        response = await self.get(endpoint="/resources/")
        return response

    async def get_item(self, code: str) -> dict | list:
        response = await self.get(endpoint=f"/items/{code}")
        data = response
        if data:
            return data
        else:
            print(f"Incorrect code {code}")

    async def get_items(
            self,
            craft_skill: str="",
            max_level: int = 30,
            min_lvl: int = 0,
            item_type: str="",
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
            params.update({"page": page})
        result = []
        if params:
            if page != 0:
                response = await self.get(
                    endpoint=endpoint,
                    params=params
                )
                return response
            else:
                for page in range(1, 5):
                    result += await self.get(
                        endpoint=endpoint,
                        params={**params,
                                "page": page}
                    )
            return result
        else:
            response = await self.get(
                endpoint=endpoint
            )
            return response

    async def get_exchange_items(self) -> dict | list:
        response = await self.get(endpoint="/ge/")
        return response

    async def get_maps(self, content: str) -> dict | list:
        response = await self.get(
            endpoint="/maps/",
            params={"content_code": content})
        return response

    async def get_map(self, x: int, y: int) -> dict | list:
        response = await self.get(endpoint=f"/maps/{x}/{y}")
        return response

    async def get_monster_coord(self, name: str) -> dict | list:
        monsters = await self.get_maps(name)
        return {"x": monsters[0].get("x"), "y": monsters[0].get("y")}

    def count_items_in_game(self, code: str) -> int:
        result = 0
        result += self.bank.items.get(code, 0)
        for player in self.players:
            for slot in SLOT_TYPES:
                if eval(f"player.{slot}") == code:
                    result += 1
            for in_slot in player.inventory:
                if in_slot.get("code") == code:
                    result += in_slot.get("quantity")
        return result

    def max_skill_level(self, code: str) -> int:
        craftable = self.items[code].craft
        if craftable:
            skill = craftable.get("skill")
            result = []
            for player in self.players:
                result.append(eval(f"player.{skill}_level"))
            return max(result)
        return 100

    def check_expired_items(self, code: str) -> bool:
        if self.items[code].level < self.max_skill_level(code) - 5:
            item_components = self.items[code].craft
            if item_components:
                if not "jasper_crystal" in [item["code"] for item in item_components["items"]]:
                    return True
            else:
                return True
        return False


if __name__ == '__main__':
    print("It's not executable file")
