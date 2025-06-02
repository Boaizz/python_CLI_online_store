from shipment.pickup import Pickup
from shipment.delivery import Delivery
from order.order import Order
from shipment.shipment import Shipment

class ShipmentFactory:
    @staticmethod
    def create_shipment(shipment_type: str, order: Order, address: str = None) -> Shipment:
        if shipment_type.lower() == "pickup":
            return Pickup(order)
        elif shipment_type.lower() == "delivery":
            return Delivery(order, address)
        else:
            raise ValueError(f"Unknown shipment type: {shipment_type}")
