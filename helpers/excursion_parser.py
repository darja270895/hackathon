from hackathon.helpers.parser import Parser


class Sputnik8(Parser):
    base_url = 'https://api.sputnik8.com/v1/'
    params = r'api_key=9bc84ec26f47bf3005dc55434b4b796a' \
             r'&username=partners+tpo50@sputnik8.com'

    @property
    def excursion_url(self) -> str:
        return f'{self.base_url}products?{self.params}'

    @property
    def cities_url(self) -> str:
        return f'{self.base_url}cities?{self.params}'

    @property
    def country_url(self) -> str:
        return f'{self.base_url}countries?{self.params}'

    @property
    def categories_url(self) -> str:
        return f'{self.base_url}cities/1/categories?{self.params}'

    async def get_excursions(self, params: dict = None) -> dict:
        """ Get excursions data by params.

        :param params: params for request.
        :return:       dict with excursions data.
        """
        resp = await self.get(url=self.excursion_url,
                              params=params)
        return resp.json()

    async def get_cities(self, params: dict = None) -> dict:
        """ Get cities data by params.

        :param params: params for request.
        :return:       dict with cities data.
        """
        resp = await self.get(url=self.cities_url,
                              params=params)
        return resp.json()

    async def get_countries(self, params: dict = None) -> dict:
        """ Get countries data by params.

        :param params: params for request.
        :return:       dict with countries data.
        """
        resp = await self.get(url=self.country_url,
                              params=params)

        return resp.json()

    async def get_categories(self, params: dict = None) -> dict:
        """ Get categories data by params.

        :param params: params for request.
        :return:       dict with categories data.
        """
        resp = await self.get(url=self.categories_url,
                              params=params)
        return resp.json()
