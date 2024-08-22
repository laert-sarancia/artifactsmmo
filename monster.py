class Monster:
    def __init__(
            self,
            name: str,
            code: str,
            level: int,
            hp: int,
            attack_fire: int,
            attack_earth: int,
            attack_water: int,
            attack_air: int,
            res_fire: int,
            res_earth: int,
            res_water: int,
            res_air: int,
            min_gold: int,
            max_gold: int,
            drops: list[dict]
    ):
        self.name = name
        self.code = code
        self.level = level
        self.hp = hp
        self.attack_fire = attack_fire
        self.attack_earth = attack_earth
        self.attack_water = attack_water
        self.attack_air = attack_air
        self.res_fire = res_fire
        self.res_earth = res_earth
        self.res_water = res_water
        self.res_air = res_air
        self.min_gold = min_gold
        self.max_gold = max_gold
        self.drops = drops

    def __repr__(self):
        return self.code

    def get_res(self):
        return {
            "fire": self.res_fire,
            "earth": self.res_earth,
            "water": self.res_water,
            "air": self.res_air,
        }

    def get_attack(self):
        return {
            "fire": self.attack_fire,
            "earth": self.attack_earth,
            "water": self.attack_water,
            "air": self.attack_air,
        }


if __name__ == '__main__':
    print("It's not executable file")
