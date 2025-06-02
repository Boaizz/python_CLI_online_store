from abc import ABC, abstractmethod
from order.order import Order

class Shipment(ABC):
    def __init__(self, order: Order):
        self.order = order
        self.status = "Pending"

    @abstractmethod
    def process(self):
        ...