from abc import ABC, abstractmethod
from typing import Dict

from models.raw import Raw
from service.raw_service import create_raw_object


class ParserStrategy(ABC):
    @abstractmethod
    def run(self, data: Raw):
        pass


class Context:
    def __init__(self, strategy: ParserStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ParserStrategy):
        self._strategy = strategy

    def run_strategy(self, data: Raw):
        return self._strategy.run(data)
