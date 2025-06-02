from shipment.shipment import Shipment


class Pickup(Shipment):
    def process(self):
        self.status = "Ready for pickup"
        print(f"Order #{self.order.order_id} is ready for pickup at store! Please visit the store to collect your order.")