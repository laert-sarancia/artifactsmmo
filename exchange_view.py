import time
from base_api import API


class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class Exchange(API):
    def __init__(self, game):
        self.game = game
        items = self.game.items
        self.craftable_items = [item for item in items if items[item].craft]

    def get_ge(self) -> list:
        response = []
        for i in range(1, 5):
            response += self.get(endpoint="/ge",
                                 params={"page": i})
        return response

    def get_item(self, code):
        response = self.get(endpoint=f"/items/{code}")
        return response

    def get_items(self):
        endpoint = "/items/"
        result = []
        for page in range(1, 5):
            result += self.get(
                endpoint=endpoint,
                params={"page": page}
            )
        return result

    def calc_item(self, code: str, buy: bool = True):
        response = self.get_item(code)
        ge = response.get("ge")
        if ge:
            sell_price = ge.get("sell_price")
            buy_price = ge.get("buy_price")
        else:
            sell_price = 0
            buy_price = 0
        buy_summ = 0
        sell_summ = 0
        craft = response["item"].get("craft")
        if craft:
            for i in craft["items"]:
                code_i = i.get("code")
                qty = i.get("quantity")
                component = self.get_item(code_i)
                component_price = component.get("ge")
                if component_price:
                    buy_component = ge.get("buy_price") * qty
                    sell_component = ge.get("sell_price") * qty
                else:
                    buy_component = 0
                    sell_component = 0
                buy_summ += buy_component
                sell_summ += sell_component
            else:
                if buy:
                    return buy_summ, sell_price
                else:
                    return buy_price, sell_summ * 20 // 100
        else:
            if buy:
                return buy_price, sell_price
            else:
                return buy_price, sell_price

    def compare(self, code: str, buy: bool = True):
        if code in ["wooden_stick", "wooden_staff"]:
            items_buy = 0
            item_sell = 0
        else:
            items_buy, item_sell = self.calc_item(code, buy)
        fix = Color.GREEN if item_sell - items_buy > 0 else Color.RED
        # if item_sell - items_buy > 0:
        print(f"{fix}{items_buy:>8} | {item_sell:<8} | "
              f"{item_sell - items_buy:<8} | {code:<8}{Color.END}")


if __name__ == '__main__':
    ex = Exchange()
    level = 5
    buy = False
    while True:
        for level in range(5, 11, 5):
            print(f"{'-'*5}{level=}{'-'*10}")
            print("BUY".rjust(8), "SELL".ljust(8), "SWAP".ljust(8), "CODE", sep=" | ")
            for code in ex.craftable_items:
                if level - 4 <= ex.items[code].get("level") <= level:
                    ex.compare(code, buy)
        time.sleep(120)
    # ex.best_trade()
    # pprint(ex.bb_items())
    # pprint(ex.bo_items())
