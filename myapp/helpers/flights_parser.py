from .parser import Parser
from .configs.config import aviasales_token


class AviasalesParser(Parser):
    @property
    def base_url(self) -> str:
        return r'http://api.travelpayouts.com/v2/prices/latest?'

    @property
    def country_url(self):
        return r'http://api.travelpayouts.com/data/cities.json'

    @property
    def aviasales_headers(self) -> dict:
        return {'x-access-token': aviasales_token}

    async def get_flights(self, params: dict) -> dict:
        """ Get all flights by params.

        :param params: dict with data
                       Example: {'origin': 'MOW',
                                 'destination': 'LED',
                                 'depart_date': '2019-11',
                                 'return_date': '2019-12',
                                 ...
                                 }
        :return:       list of flights.
        """
        resp = await self.get(url=self.base_url,
                              headers=self.aviasales_headers,
                              params=params)
        return resp.json().get('data', list)

    async def get_countries(self) -> dict:
        """ Get info about countries.

        :param params: dict with data
        :return: dict with countries data.
        """
        resp = await self.get(url=self.country_url)
        return resp.json()
