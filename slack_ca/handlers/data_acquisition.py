import requests
import json
import logging

from abc import abstractmethod, ABCMeta


class IDataAcquisition(object, metaclass=ABCMeta):
    @abstractmethod
    def fetch(self):
        """
        Covert a list of data to use
        :param endpoint: endpoint to connect to
        :return: list of models
        """
        return []

class BaseDataAcquisition(IDataAcquisition, metaclass=ABCMeta):
    def fetch(self):
        pass

    @abstractmethod
    def create_request_for_page(self, page):
        """
        Create a HttpRequest for fetching a page
        :param page: the page to fetch
        :return: the request
        """
        return requests.Response()
