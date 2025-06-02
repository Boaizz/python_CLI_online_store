from datetime import datetime
from user.customer import Customer
from cart.shoppingCart import ShoppingCart
from observer.subject import Subject
from order.orderItem import OrderItem

class Order(Subject):
    def __init__(self, order_id: int, customer: Customer, cart: ShoppingCart):
        super().__init__()
        self.order_id = order_id
        self.customer = customer
        self.order_items: list[OrderItem] = [
            OrderItem(ci.product, ci.qty) for ci in cart.items.values()
        ]
        self.status = "Created"
        self.created_at = datetime.now()
        self.payment = None
        self.shipment = None

    def summary(self):
        print(f"\nOrder #{self.order_id} for {self.customer.name}")
        print("Items:")
        for oi in self.order_items:
            print(f"  {oi.product.name} × {oi.qty} = ${oi.total_price():.2f}")
        total = sum(oi.total_price() for oi in self.order_items)
        print(f"Total amount: ${total:.2f}")
        print(f"Status: {self.status}\n")