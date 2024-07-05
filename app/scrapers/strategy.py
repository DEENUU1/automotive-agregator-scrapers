from abc import ABC, abstractmethod


class ScraperStrategy(ABC):
    @abstractmethod
    def run(self):
        pass


class Context:
    def __init__(self, strategy: ScraperStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ScraperStrategy):
        self._strategy = strategy

    def run_strategy(self):
        self._strategy.run()
