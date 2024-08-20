import asyncio
from game import Game


async def main():
    game = Game()
    await asyncio.gather(
        game.lert.main_mode(),
        game.ralernan.work_helper_mode0(),
        game.kerry.work_helper_mode1(),
        game.karven.work_helper_mode2(),
        game.warrant.work_helper_mode3(),
    )


if __name__ == '__main__':
    asyncio.run(main())
