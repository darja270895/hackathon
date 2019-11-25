from hackathon.helpers.parser import Parser, loop


class TravelataParser(Parser):
    base_url = 'http://api-gateway.travelata.ru/'

    @property
    def cheapest_tours_url(self) -> str:
        return f'{self.base_url}statistic/cheapestTours'

    @property
    def country_url(self) -> str:
        return f'{self.base_url}directory/countries'

    @property
    def hotel_url(self) -> str:
        return f'{self.base_url}directory/resortHotels'

    @property
    def hotel_categories_url(self) -> str:
        return f'{self.base_url}directory/hotelCategories'

    @property
    def resorts_url(self) -> str:
        return f'{self.base_url}directory/resorts'

    async def get_cheapest_tours(self, params: dict = None) -> dict:
        """ Get cheapest tours.

        :param params: params for request.
        :return:       dict with cheapest tours data.
        """
        resp = await self.get(url=self.cheapest_tours_url,
                              params=params)
        return resp.json()

    async def get_countries(self, params: dict = None) -> dict:
        """ Get data about countries.

        :param params: params for request.
        :return:       dict with countries data.
        """
        resp = await self.get(url=self.country_url,
                              params=params)
        return resp.json()

    async def get_hotels(self, params: dict = None) -> dict:
        """ Get data about hotels.

        :param params: params for request.
        :return:       dict with hotels data.
        """
        resp = await self.get(url=self.hotel_url,
                              params=params)
        return resp.json()

    async def get_hotel_categories(self, params: dict = None) -> dict:
        """ Get data with hotels categories.

        :param params: params for request.
        :return:       dict with hotels categories.
        """
        resp = await self.get(url=self.hotel_categories_url,
                              params=params)
        return resp.json()

    async def get_resorts(self, params: dict = None) -> dict:
        """ Get resorts info.

        :param params: params for request.
        :return:       dict with resorts.
        """
        resp = await self.get(url=self.resorts_url,
                              params=params)
        return resp.json()
