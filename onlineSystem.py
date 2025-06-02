from datetime import date
import os
import sys
from cart.shoppingCart import ShoppingCart
from payment.cardDetails import CardDetails
from payment.receipt import Receipt
from user.customer import Customer
from order.orderManagement import OrderManagement
from product.product import Product
from product.productCatalogue import ProductCatalogue
from shipment.shipmentFactory import ShipmentFactory
from statistic.statistic import Statistic
from observer.warehouse import Warehouse


class OnlineSystem:
    PRODUCT_FILE = "product.txt"
    USER_FILE    = "user.txt"

    def __init__(self):
        self.catalogue        = ProductCatalogue()
        self.warehouse        = Warehouse()
        self.stats            = Statistic()
        self.order_manager    = OrderManagement(self.warehouse, self.stats)
        self.customers        = {}
        self.next_order_id    = 1
        self.current_customer = None
        self.cart             = ShoppingCart()

        self.load_users_from_file()
        if 0 not in self.customers:
            admin = Customer(0, "Admin", "Admin", "admin", True)
            self.customers[0] = admin
            self.save_users_to_file()

        self.load_products_from_file()

    def load_users_from_file(self):
        if os.path.exists(self.USER_FILE):
            with open(self.USER_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    cid, name, email, pw, is_admin = line.split("|")
                    user = Customer(int(cid), name, email, pw, is_admin == "True")
                    self.customers[user.customer_id] = user

    def save_users_to_file(self):
        with open(self.USER_FILE, "w", encoding="utf-8") as f:
            for u in sorted(self.customers.values(), key=lambda x: x.customer_id):
                line = "|".join([
                    str(u.customer_id),
                    u.name,
                    u.email,
                    u._password,
                    str(u.isAdmin)
                ])
                f.write(line + "\n")

    def load_products_from_file(self):
        if os.path.exists(self.PRODUCT_FILE):
            with open(self.PRODUCT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    pid, name, desc, price, stock_str = line.split("|")
                    stock = 0 if stock_str == "Unavailable" else int(stock_str)
                    self.catalogue.add_product(Product(int(pid), name, desc, float(price), stock))
        else:
            for pid,name,desc,price,stock in [
                (1,"Smartphone","5G",699.99,50),
                (2,"Laptop","Ultrabook",1299.99,20),
                (3,"Earbuds","Noise-cancelling",199.99,100),
                (4,"Watch","Smartwatch",249.99,75),
            ]:
                self.catalogue.add_product(Product(pid,name,desc,price,stock))
            self.save_products_to_file()

    def save_products_to_file(self):
        with open(self.PRODUCT_FILE, "w", encoding="utf-8") as f:
            for p in sorted(self.catalogue.products.values(), key=lambda x: x.product_id):
                stock_str = str(p.stock) if p.stock > 0 else "Unavailable"
                line = "|".join([
                    str(p.product_id),
                    p.name,
                    p.description,
                    f"{p.price:.2f}",
                    stock_str
                ])
                f.write(line + "\n")

    def register_customer(self):
        email = input("Email: ").strip()
        if any(u.email == email for u in self.customers.values()):
            print("User already exists.\n")
            return
        cid   = max(self.customers.keys(), default=0) + 1
        name  = input("Name: ").strip()
        pw    = input("Password: ").strip()
        c     = Customer(cid, name, email, pw)
        self.customers[cid] = c
        self.save_users_to_file()
        print(f"Registered: {c}\n")

    def login(self) -> bool:
        email = input("Email: ").strip()
        pw    = input("Password: ").strip()
        user = next((u for u in self.customers.values() if u.email == email), None)
        if user:
            if user.check_password(pw):
                self.current_customer = user
                print(f"Welcome, {user.name}\n")
                return True
            else:
                print("Wrong password.\n")
                return False
        print("User not found.\n")
        print("Want to register? 1) Yes  2) No")
        choice = input("Choose: ").strip()
        if choice == "1":
            self.register_customer()
        return False

    def browse(self):
        print("\nProducts:")
        self.catalogue.list_products()
        print()

    def add_to_cart(self):
        try:
            pid  = int(input("Product ID: "))
            prod = self.catalogue.get(pid)
            qty  = int(input("Quantity: "))
            if not prod or not prod.reduce_stock(qty):
                print("Invalid product or insufficient stock.\n")
                return
            self.cart.add_item(prod, qty)
        except:
            print("Input error.\n")

    def remove_from_cart(self):
        try:
            pid = int(input("Product ID to remove: "))
            self.cart.remove_item(pid)
        except:
            print("Input error.\n")

    def view_cart(self):
        self.cart.view_cart()
        print()

    def checkout(self):
        if not self.cart.items:
            print("Cart empty.\n")
            return
        oid = self.next_order_id; self.next_order_id += 1
        order = self.order_manager.create_order(oid, self.current_customer, self.cart)
        order.summary()

        card = input("Card#16: ").strip()
        exp  = input("Expiry MM/YY: ").strip()
        cvv  = input("CVV3: ").strip()
        pd   = CardDetails(oid, self.cart.calculate_total(), card, exp, cvv)
        if not pd.validate():
            print("Card invalid.\n")
            return
        if not self.order_manager.process_payment(order, pd):
            return

        print("1) Pickup   2) Delivery")
        choice = input("Choose shipment: ").strip()
        if choice == "1":
            sh = ShipmentFactory.create_shipment("pickup", order)
        elif choice == "2":
            addr = input("Delivery address: ").strip()
            sh = ShipmentFactory.create_shipment("delivery", order, addr)
        else:
            print("Invalid shipment choice.\n")
            return
        self.order_manager.ship_order(order, sh)
        self.order_manager.complete_order(order)
                                                                                                                                                                                         
        self.save_products_to_file()

        self.cart = ShoppingCart()
        Receipt(order).print_receipt()

    def sales_report(self):
        if not self.current_customer or not self.current_customer.isAdmin:
            print("🚫 Permission denied: admin only.\n")
            return
        d = date.today()
        day_sales = self.stats.daily_sales.get(d, {})
        lines = [f"Sales Report for {d.isoformat()}:"]
        if not day_sales:
            lines.append("  No sales recorded.")
        else:
            for pid, qty in day_sales.items():
                lines.append(f"  Product {pid}: {qty} unit(s) sold")
        with open("sales.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        for line in lines:
            print(line)

    def modify_catalogue(self):
        if not self.current_customer or not self.current_customer.isAdmin:
            print("🚫 Permission denied: admin only.\n")
            return
        print("1) Add product   2) Remove product   3) Update product")
        choice = input("Choice: ").strip()
        if choice == "1":
            try:
                pid = int(input("New Product ID: "))
                if pid in self.catalogue.products:
                    print("Product already exists.\n")
                    return
                name  = input("Name: ").strip()
                desc  = input("Description: ").strip()
                price = float(input("Price: "))
                stck  = int(input("Stock: "))
                self.catalogue.add_product(Product(pid, name, desc, price, stck))
                self.save_products_to_file()
                print("Product added and saved.\n")
            except:
                print("Invalid input.\n")
        elif choice == "2":
            try:
                pid = int(input("Product ID to remove: "))
                if pid in self.catalogue.products:
                    self.catalogue.remove_product(pid)
                    self.save_products_to_file()
                    print("Product removed and changes saved.\n")
                else:
                    print("Not found.\n")
            except:
                print("Input error.\n")
        elif choice == "3":
            try:
                pid = int(input("Product ID to update: "))
                p = self.catalogue.get(pid)
                if not p:
                    print("Product not found.\n")
                    return
                new_desc  = input(f"New description [{p.description}]: ").strip() or p.description
                new_price = input(f"New price [{p.price}]: ").strip()
                new_stock = input(f"New stock [{p.stock}]: ").strip()

                p.description = new_desc
                if new_price:
                    p.price = float(new_price)
                if new_stock:
                    p.stock = int(new_stock)

                self.save_products_to_file()
                print("Product updated and saved.\n")
            except Exception:
                print("Invalid input.\n")
        else:
             print("Cancelled.\n")

    def run(self):
        print("---------------------------------------\n")
        print("Welcome to AWE Electronics Online Store\n")
        print("---------------------------------------\n")
        while True: 
            while True:
                print("1) Register  2) Login  3) Exit")
                c = input("Choose:").upper()
                if c == "1":
                    self.register_customer()
                elif c == "2" and self.login():
                    break
                elif c == "3":
                    sys.exit(0)

            while True:
                if self.current_customer and self.current_customer.isAdmin:
                    # admin menu: hide user-only actions
                    print("1) Browse All Products   8) Sales Report (admin)   9) Modify Catalogue (admin)   0) Logout/Exit")
                else:
                    # regular customer menu
                    print("1) Browse All Products   2) Filter Products   3) View Product Details")
                    print("4) Add to Cart   5) Remove from Cart   6) View Cart")
                    print("7) Checkout   8) Sales Report (admin)   9) Modify Catalogue (admin)   0) Logout/Exit")
                cmd = input("Choose: ").strip()
                if cmd == "1":
                    self.browse()
                # customer-only commands
                elif cmd == "2" and not (self.current_customer and self.current_customer.isAdmin):
                    self.filter_products()
                elif cmd == "3" and not (self.current_customer and self.current_customer.isAdmin):
                    self.get_product_details()
                elif cmd == "4" and not (self.current_customer and self.current_customer.isAdmin):
                    self.add_to_cart()
                elif cmd == "5" and not (self.current_customer and self.current_customer.isAdmin):
                    self.remove_from_cart()
                elif cmd == "6" and not (self.current_customer and self.current_customer.isAdmin):
                    self.view_cart()
                elif cmd == "7" and not (self.current_customer and self.current_customer.isAdmin):
                    self.checkout()
                elif cmd == "8":
                    self.sales_report()
                elif cmd == "9":
                    self.modify_catalogue()
                elif cmd == "0":
                    print("Logged out.\n")
                    self.current_customer = None
                    self.cart = ShoppingCart()
                    self.catalogue = ProductCatalogue()
                    self.load_products_from_file()
                    break 

    def filter_products(self):
        term = input("Enter search term: ").strip().lower()
        matches = [
            p for p in self.catalogue.products.values()
            if term in p.name.lower() or term in p.description.lower()
        ]
        if not matches:
            print("No products match your search.\n")
            return
        print("\nSearch Results:")
        for p in matches:
            print(p)
        print()

    def get_product_details(self):
        try:
            pid = int(input("Enter Product ID to view details: "))
            p = self.catalogue.get(pid)
            if p:
                print(f"\nID: {p.product_id}")
                print(f"Name: {p.name}")
                print(f"Description: {p.description}")
                print(f"Price: ${p.price:.2f}")
                print(f"Stock: {p.stock}\n")
            else:
                print("Product not found.\n")
        except:
            print("Input error.\n")
