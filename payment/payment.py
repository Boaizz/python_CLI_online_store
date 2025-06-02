class Payment:
    def __init__(self, order_id: int, amount: float):
        self.order_id = order_id
        self.amount = amount
        self.status = "Pending"

    def process(self) -> bool:
        print(f"Processing payment of ${self.amount:.2f} for Order #{self.order_id}...")
        self.status = "Paid"
        return True