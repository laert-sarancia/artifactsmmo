import asyncio
from game import Game


async def main():
    game = await Game()
    await asyncio.gather(
        game.lert.play_role(),
        game.ralernan.play_role(),
        game.kerry.play_role(),
        game.karven.play_role(),
        game.warrant.play_role(),
    )


if __name__ == '__main__':
    asyncio.run(main())
