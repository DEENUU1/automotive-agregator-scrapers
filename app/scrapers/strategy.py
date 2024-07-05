from abc import ABC, abstractmethod
from typing import Dict
from service.raw_service import create_raw_object


class ScraperStrategy(ABC):
    @abstractmethod
    def run(self):
        pass

    @staticmethod
    async def save_raw(raw: Dict):
        result = await create_raw_object(raw)
        return result


class Context:
    def __init__(self, strategy: ScraperStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ScraperStrategy):
        self._strategy = strategy

    def run_strategy(self):
        self._strategy.run()
