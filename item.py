class Item:
    def __init__(
            self,
            name: str,
            code: str,
            level: int,
            type: str,
            subtype: str,
            description: str,
            effects: list[dict],
            craft: None | dict
    ):
        self.name = name
        self.code = code
        self.level = level
        self.i_type = type
        self.subtype = subtype
        self.description = description
        self.effects = effects
        self.craft = craft

    def __repr__(self):
        return self.code


if __name__ == '__main__':
    print("It's not executable file")
