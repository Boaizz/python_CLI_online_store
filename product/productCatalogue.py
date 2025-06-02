from product.product import Product

class ProductCatalogue:
    def __init__(self):
        self.products: dict[int, Product] = {}

    def add_product(self, p: Product):
        self.products[p.product_id] = p

    def remove_product(self, pid: int):
        if pid in self.products:
            del self.products[pid]

    def list_products(self):
        for p in sorted(self.products.values(), key=lambda x: x.product_id):
            print(p)

    def get(self, pid: int) -> Product | None:
        return self.products.get(pid)