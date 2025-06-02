from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, order, event: str):
        pass