from abc import abstractmethod
from enum import Enum


class ServiceMode(Enum):
    LOCAL = 1
    AWS = 2

class Service(object):
    """
    Abstract class for All Microservices
    """

    def __init__(self, name=None):
        if name:
            self.name = name
