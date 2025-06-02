
GREEN = '\033[92m'
RED   = '\033[91m'
RESET = '\033[0m'

class Product:
    def __init__(self, product_id: int, name: str, description: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def __str__(self):
        if self.stock > 0:
            return (f"[{self.product_id}] {self.name} – ${self.price:.2f} "
                    f"({self.stock} in stock – {GREEN}available{RESET})")
        else:
            return f"[{self.product_id}] {self.name} – ${self.price:.2f} ({RED}unavailable{RESET})"

    def reduce_stock(self, qty: int) -> bool:
        if qty <= self.stock:
            self.stock -= qty
            return True
        return False