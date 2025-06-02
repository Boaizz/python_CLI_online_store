from payment.payment import Payment

class CardDetails(Payment):
    def __init__(self, order_id: int, amount: float, card_number: str, expiry: str, cvv: str):
        super().__init__(order_id, amount)
        self.card_number = card_number
        self.expiry = expiry
        self.cvv = cvv

    def validate(self) -> bool:
        print("Validating card details...")
        return len(self.card_number) == 10 and len(self.cvv) == 3