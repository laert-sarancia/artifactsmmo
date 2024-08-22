import json
import time
import logging
import requests
from dotenv import dotenv_values
logging.basicConfig(filename=f"logs/log_{time.time()}.log", level=logging.INFO)


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(msg=f"lag: {end_time - start_time:.2f} {kwargs}")
        # print(f"lag: {end_time - start_time:.2f} {kwargs}")
        return result
    return wrapper


class Base:
    def get(
            self,
            endpoint: str,
            data: dict | None = None,
            params: dict | None = None,
    ) -> dict:
        """
        Метод для получения данных
        :param endpoint: путь до данных
        :param data: фильтр для данных
        :param params:
        :return: словарь с результатами
        """
        pass

    def post(
            self,
            endpoint: str,
            data: dict | None = None,
            params: dict | None = None
    ) -> dict:
        """
        Метод для отправки данных
        :param endpoint: путь до данных
        :param data: передаваемые данные
        :param params: передаваемые данные
        :return:
        """
        pass


class API(Base):
    base_url = f"https://api.artifactsmmo.com"
    __config = dotenv_values("game.env")
    __token = __config["ARTIFACTS_TOKEN"]
    __headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {__token}"
    }

    @time_it
    def get(
            self,
            endpoint: str,
            data: dict | None = None,
            params: dict | None = None,
    ) -> dict:
        response = requests.get(
            self.base_url + endpoint,
            headers=self.__headers,
            data=data,
            params=params
        )
        if response.status_code == 404:
            return {}
        else:
            return response.json().get("data")

    @time_it
    def post(
            self,
            endpoint: str,
            data: dict | None = None,
            params: dict | None = None
    ) -> dict:
        response = requests.post(
            self.base_url + endpoint,
            headers=self.__headers,
            data=json.dumps(data),
            params=json.dumps(params)
        )
        if response.status_code == 404:
            return {}
        elif response.status_code == 499:
            time.sleep(10)
            response = requests.post(
                self.base_url + endpoint,
                headers=self.__headers,
                data=json.dumps(data),
                params=json.dumps(params)
            )
        response.raise_for_status()
        return response.json().get("data")


if __name__ == '__main__':
    print("It's not executable file")
