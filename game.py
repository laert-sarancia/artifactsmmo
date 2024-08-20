from player import Player
from base_api import API


class Game(API):
    def __init__(self):
        super().__init__()
        self.items = {item["code"]: item for item in self.get_items(page=0)}
        self.monsters = {item["code"]: item for item in self.get_monsters()}

        self.lert = Player(name="Lert", game=self)
        self.ralernan = Player(name="Ralernan", game=self)
        self.kerry = Player(name="Kerry", game=self)
        self.karven = Player(name="Karven", game=self)
        self.warrant = Player(name="Warrant", game=self)

    def __repr__(self) -> str:
        return "artifactsmmo"

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


if __name__ == '__main__':
    print("It's not executable file")
