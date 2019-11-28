from .helpers.booking_parser import Hotellook
from .helpers.excursion_parser import Sputnik8, Tripster
from .helpers.flights_parser import AviasalesParser

booking_instance = Hotellook()
excursion_instance = Sputnik8()
flights_instance = AviasalesParser()
tripster_instance = Tripster()


class TourManager:
    @staticmethod
    async def excursion_by_city_search(city_name: str, lang='en', limit=10) -> dict:
        """ Get excursions by city name.

        :param country_name: name of the city.
        :param lang:         language.
        :param limit:        excursions count.
        :return:             dict with excursions.
        """
        city_params = {'lang': lang, 'name': city_name, 'limit': 100}
        cities = await excursion_instance.get_cities(city_params)
        for city in cities:
            if city.get('name') == city_name:
                data = {'city_id': city.get('region_id'),
                        'country_id': city.get('country_id'),
                        'limit': limit}
                return await excursion_instance.get_excursions(data)

    @staticmethod
    async def excursion_by_country_search(country_name: str, lang='en', limit=10) -> dict:
        """ Get excursions by country name.

        :param country_name: name of the country.
        :param lang:         language.
        :param limit:        excursions count.
        :return:             dict with excursions.
        """
        city_params = {'lang': lang, 'limit': 100}
        countries = await excursion_instance.get_countries(city_params)
        for country in countries:
            if country.get('name') == country_name:
                data = {'country_id': country.get('id'),
                        'limit': limit}
                return await excursion_instance.get_excursions(data)

    @staticmethod
    async def get_hotels(query: str, limit: int, lang: str) -> list:
        """ Get list of hotels by query.

        :param query: country name or city name.
        :param limit: count of hotels.
        :param lang:  en/ru.
        :return:      list of hotels.
        """
        data = {'query': query,
                'lang': lang,
                'lookFor': 'hotel',
                'limit': limit}
        resp = await booking_instance.get_hotels(data)
        results = resp.get('results')
        return results.get('hotels')

    @staticmethod
    async def get_city_excursions(city_name: str) -> dict:
        """ Get excursions by RUS city name.

        :param city_name: name of the city in RUS.
        :return:          dict with excursions.
        """
        return await tripster_instance.get_trip(city_name)

    async def get_country_tour(self, flights_params, country_name,
                               lang='en', limit=1) -> tuple:
        """ Get tour by country name.

        :param flights_params: params for aviasales API.
        :param country_name:   name of the country.
        :param lang:           language.
        :param limit:          count of instances.
        :return:               tuple(excursions, flights, hotels)
        """
        excursions = await self.excursion_by_country_search(country_name, limit=limit)
        flights = await flights_instance.get_flights(flights_params)
        hotels = await self.get_hotels(query=country_name, limit=limit, lang=lang)
        return excursions, flights, hotels

    async def get_city_tour(self, flights_params, city_name, lang='en', limit=1) -> tuple:
        """ Get tour by city name.

        :param flights_params: params for aviasales API.
        :param city_name:      name of the city.
        :param lang:           language.
        :param limit:          count of instances.
        :return:               tuple(excursions, flights, hotels)
        """
        excursions = await self.excursion_by_city_search(city_name, limit=limit)
        flights = await flights_instance.get_flights(flights_params)
        hotels = await self.get_hotels(query=city_name, limit=limit, lang=lang)
        return excursions, flights, hotels

