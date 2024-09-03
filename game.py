from dataclasses import dataclass

from parameters import SLOT_TYPES
from player import Player
from monster import Monster
from item import Item
from base_api import API
from exchange_view import Exchange


@dataclass
class Bank:
    def __init__(self, game):
        self.game = game
        self.money = self.game.get_bank_details()["gold"]
        self.slots = self.game.get_bank_details()["slots"]
        self.expansions = self.game.get_bank_details()["expansions"]
        self.next_expansion_cost = self.game.get_bank_details()["next_expansion_cost"]
        self.items: dict[str, int] = {item["code"]: item["quantity"] for item in self.game.get_bank_items(page=0)}

    def update_bank(self, **kwargs):
        self.__dict__.update(**kwargs)


@dataclass
class Game(API):
    def __init__(self):
        super().__init__()
        self.items: dict[str: Item] = {item["code"]: Item(**item) for item in self.get_items(page=0)}
        self.monsters: dict[str, Monster] = {mon["code"]: Monster(**mon) for mon in self.get_monsters()}
        self.bank = Bank(self)
        self.exchange = Exchange(self)
        self.lert = Player(game=self, **self.get_character("Lert"))
        self.ralernan = Player(game=self, **self.get_character("Ralernan"))
        self.kerry = Player(game=self, **self.get_character("Kerry"))
        self.karven = Player(game=self, **self.get_character("Karven"))
        self.warrant = Player(game=self, **self.get_character("Warrant"))
        self.players = [self.lert, self.ralernan, self.kerry, self.karven, self.warrant]

    # ******* GAME ACTIONS ****** #

    def update_bank(self):
        self.bank.update_bank(**self.get_bank_details())

    def get_status(self):
        response = self.get("/")
        return response

    def get_character(self, name) -> dict | list:
        response = self.get(endpoint=f"/characters/{name}")
        return response

    def get_bank_items(
            self,
            code: str | None = None,
            page: int = 1
    ) -> dict | list:
        endpoint = "/my/bank/items"
        params = {"item_code": code}
        if code:
            params.update({"code": code})
        if page:
            params.update({"page": page})

        if page != 0:
            result = self.get(
                endpoint=endpoint,
                params=params
            )
        else:
            result = []
            for page in range(1, 5):
                result += self.get(
                    endpoint=endpoint,
                    params={**params,
                            "page": page}
                )
        return result

    def get_bank_details(self) -> dict | list:
        response = self.get(endpoint="/my/bank")
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

    def get_resources(self) -> dict | list:
        response = self.get(endpoint="/resources/")
        return response

    def get_item(self, code: str) -> dict | list:
        response = self.get(endpoint=f"/items/{code}")
        data = response
        if data:
            return data
        else:
            print(f"Incorrect code {code}")

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
            params.update({"page": page})
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

    def max_skill_level(self, code) -> int:
        craftable = self.items[code].craft
        if craftable:
            skill = craftable.get("skill")
            result = []
            for player in self.players:
                result.append(eval(f"player.{skill}_level"))
            return max(result)
        return 100

    def check_expired_items(self, code: str) -> bool:
        return True if self.items[code].level < self.max_skill_level(code) - 5 else False


if __name__ == '__main__':
    print("It's not executable file")
