from product.product import Product


class CartItem:
    def __init__(self, product: Product, qty: int):
        self.product = product
        self.qty = qty

    def total_price(self) -> float:
        return self.product.price * self.qty