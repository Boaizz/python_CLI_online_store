from product.product import Product

class OrderItem:
    def __init__(self, product: Product, qty: int):
        self.product = product
        self.qty = qty

    def total_price(self) -> float:
        return self.product.price * self.qty
