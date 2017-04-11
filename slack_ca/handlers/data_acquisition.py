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
    def __init__(self):
        pass

    def fetch(self):
        pass
