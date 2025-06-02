from cart.cartItem import CartItem
from product.product import Product


class ShoppingCart:
    def __init__(self):
        self.items: dict[int, CartItem] = {}

    def add_item(self, product: Product, qty: int):
        if product.product_id in self.items:
            self.items[product.product_id].qty += qty
        else:
            self.items[product.product_id] = CartItem(product, qty)
        print(f"Added {qty} × {product.name} to your cart.")

    def remove_item(self, pid: int):
        if pid in self.items:
            del self.items[pid]
            print(f"Removed product {pid} from your cart.")
        else:
            print("That product is not in your cart.")

    def view_cart(self):
        if not self.items:
            print("Your cart is empty.")
            return
        total = 0.0
        print("Your Shopping Cart:")
        for ci in self.items.values():
            line = f"{ci.product.name} | qty: {ci.qty} | line total: ${ci.total_price():.2f}"
            print("  ", line)
            total += ci.total_price()
        print(f"Cart total: ${total:.2f}")

    def calculate_total(self) -> float:
        return sum(ci.total_price() for ci in self.items.values())