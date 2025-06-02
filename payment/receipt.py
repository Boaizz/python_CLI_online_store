from datetime import datetime

class Receipt:
    def __init__(self, order):
        self.order = order
        self.generated = datetime.now()

    def print_receipt(self):
        print("\n------------ RECEIPT -------------")
        print(f"Order ID: {self.order.order_id}")
        print(f"Customer: {self.order.customer.name}")
        for oi in self.order.order_items:
            print(f"{oi.product.name} × {oi.qty} = ${oi.total_price():.2f}")
        total = sum(oi.total_price() for oi in self.order.order_items)
        print(f"Total Paid: ${total:.2f}")
        print(f"Paid at: {self.generated.strftime('%Y-%m-%d %H:%M:%S')}")
        print("Thank you for shopping at AWE Electronics!!!\n")