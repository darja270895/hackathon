# !/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio

import requests_async as requests
from bs4 import BeautifulSoup

loop = asyncio.get_event_loop()


class Parser:
    def __init__(self, username: str = '', password: str = ''):
        self.session = requests.Session()
        self.session.auth = (username, password)

    async def get(self, url: str, **kwargs):
        """ Sends a GET request.

        :param url: current URL.
        :return:    class:`Response` object.
        """
        resp = await self.session.get(url, **kwargs)
        self._raise_status(resp)
        return resp

    async def post(self, url: str, data=None, json=None, **kwargs):
        """ Sends a POST request.

        :param url:    current URL.
        :param json:   (optional) json to send in the body of the :class:`Request`.
        :param kwargs: (optional) arguments that ``request`` takes.
        :param data:   (optional) Dictionary, list of tuples, bytes, or file-like
                        object to send in the body of the :class:`Request`.
        :return:       class:`Response` object.
        """
        resp = await self.session.post(url, data=data, json=json, **kwargs)
        return resp

    async def put(self, url: str, data=None, **kwargs):
        """ Sends a PUT request.

        :param url:    current URL.
        :param data:   (optional) Dictionary, list of tuples, bytes, or file-like
                        object to send in the body of the :class:`Request`.
        :param kwargs: (optional) arguments that ``request`` takes.
        :return:       class:`Response` object.
        """
        resp = await self.session.put(url, data, **kwargs)
        return resp

    @staticmethod
    def _raise_status(resp):
        """ Raises "HTTPError", if one occurred.

        :param resp: class:`Response` object.
        """
        if resp.status_code != requests.codes.ok:
            resp.raise_for_status()

    @staticmethod
    def get_soup(html_doc: str, **kwargs):
        """ Get BeautifulSoup object using html text.

        :param html_doc: html text.
        :return:         BeautifulSoup object.
        """
        return BeautifulSoup(html_doc, 'html.parser', **kwargs)

    @property
    def cookies(self):
        return self.session.cookies

    @property
    def headers(self):
        return self.session.headers

    @property
    def params(self):
        return self.session.params

    @property
    def proxies(self):
        return self.session.proxies
