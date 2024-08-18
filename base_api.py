import json
import time

import requests
from time import sleep
from datetime import datetime
from dotenv import dotenv_values


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

    def get(
            self,
            endpoint: str,
            data: dict | None = None,
            params: dict | None = None,
    ) -> dict:
        start = datetime.now()
        sleep(0.5)
        response = requests.get(
            self.base_url + endpoint,
            headers=self.__headers,
            data=data,
            params=params
        )
        end = datetime.now()
        print(f"lag: {end - start} [{endpoint}]")
        if response.status_code == 404:
            return {}
        else:
            return response.json().get("data")

    def post(
            self,
            endpoint: str,
            data: dict | None = None,
            params: dict | None = None
    ) -> dict:
        start = datetime.now()
        response = requests.post(
            self.base_url + endpoint,
            headers=self.__headers,
            data=json.dumps(data),
            params=json.dumps(params)
        )
        end = datetime.now()
        print(f"lag: {end - start} [{endpoint}]")
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
