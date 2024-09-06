import asyncio
import aiohttp
import json
import time
import logging
from dotenv import dotenv_values


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(msg=f"lag: {end_time - start_time:.2f} {kwargs}")
        # print(f"lag: {end_time - start_time:.2f} {kwargs}")
        return result

    return wrapper


class AObject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """

    async def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        await instance.__init__(*args, **kwargs)
        return instance

    async def __init__(self):
        pass


class AsyncRequester(AObject):
    base_url = f"https://api.artifactsmmo.com"
    __config = dotenv_values("game.env")
    __token = __config["ARTIFACTS_TOKEN"]
    __headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {__token}"
    }

    async def __init__(self):
        await super().__init__()

    @time_it
    async def get(
            self,
            endpoint,
            data: dict | None = None,
            params: dict | None = None,
    ):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=f"{self.base_url}{endpoint}",
                    headers=self.__headers,
                    data=data,
                    params=params
            ) as response:
                resp_data = await response.json()
                if response.status == 200:
                    resp_data = resp_data.get("data")
                elif response.status == 404:
                    resp_data = {}
                elif response.status >= 500:
                    await asyncio.sleep(60)
                    resp_data = await self.post(endpoint, data, params)
                return resp_data

    @time_it
    async def post(
            self,
            endpoint,
            data: dict | None = None,
            params: dict | None = None
    ):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self.base_url + endpoint,
                    headers=self.__headers,
                    data=json.dumps(data),
                    params=json.dumps(params)
            ) as response:
                if response.status < 500:
                    resp_data = await response.json()
                else:
                    print(response.status)
                    return {}
            error = resp_data.get("error")
            if error:
                print(error, params)
                return {}
            if response.status == 200:
                resp_data = resp_data.get("data")
            elif response.status == 404:
                resp_data = {}
            elif response.status == 499:
                cd_msg = resp_data.get("code", {}).get("message")
                if cd_msg:
                    cd = float(cd_msg.replace(" seconds left.", "").replace("Character in cooldown: ", ""))
                else:
                    cd = 10
                print(f"{endpoint} Wait {cd}sec")
                await asyncio.sleep(cd)
                await self.post(endpoint, data, params)
            elif response.status >= 500:
                await asyncio.sleep(60)
                await self.post(endpoint, data, params)
            return resp_data


if __name__ == '__main__':
    print("It's not executable file")
