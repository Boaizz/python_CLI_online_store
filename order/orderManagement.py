from user.customer import Customer
from shipment.pickup import Pickup
from shipment.shipment import Shipment
from cart.shoppingCart import ShoppingCart
from observer.warehouse import Warehouse
from observer.customerNotifier import CustomerNotifier
from statistic.statistic import Statistic
from observer.subject import Subject
from order.order import Order
from shipment.shipmentFactory import ShipmentFactory
from payment.payment import Payment
from cart.cartItem import CartItem

class OrderManagement:
    def __init__(self, warehouse: Warehouse, stats: Statistic):
        self.warehouse = warehouse
        self.stats     = stats
        self.orders    = {}

    def create_order(self, order_id: int, customer: Customer, cart: ShoppingCart) -> Order:
        order = Order(order_id, customer, cart)
        self.orders[order_id] = order
# attach observers for order status events
        order.attach(self.warehouse)
        order.attach(CustomerNotifier())
        print(f"Order #{order_id} created.")
        return order

    def process_payment(self, order: Order, payment: Payment) -> bool:
        success = payment.process()
        if success:
            order.payment = payment
            order.status = "Paid"
            print(f"Order #{order.order_id} payment succeeded.")
            order.notify_observers(order, "paid")
        else:
            print(f"Order #{order.order_id} payment failed.")
        return success

    def ship_order(self, order: Order, shipment: Shipment):
        shipment.process()
        order.shipment = shipment
        order.status   = shipment.status
        if isinstance(shipment, Pickup):
            order.notify_observers(order, "pickup")
        else:
            order.notify_observers(order, "shipped")
        self.stats.record_order(order)

    def complete_order(self, order: Order):
        order.status = "Completed"
        print(f"Order #{order.order_id} marked as completed.")
        order.notify_observers(order, "completed")