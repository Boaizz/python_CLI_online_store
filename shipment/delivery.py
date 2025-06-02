from order.order import Order
from shipment.shipment import Shipment


class Delivery(Shipment):
    def __init__(self, order: Order, address: str):
        super().__init__(order)
        self.address = address

    def process(self):
        self.status = "Out for delivery"
        print(f"Order #{self.order.order_id} is out for delivery to {self.address}. Please wait for the delivery to arrive.")