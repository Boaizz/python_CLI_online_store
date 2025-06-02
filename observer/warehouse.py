from observer.observer import Observer
from order.order import Order

class Warehouse(Observer):
    def update(self, order: Order, event: str):
        blue_blink = "\033[5;94m"  
        reset = "\033[0m"
        if event == "shipped":
            message = (
                f"Warehouse notified for Order #{order.order_id} — preparing delivery."
            )
            print(f"{blue_blink}{message}{reset}")
        elif event == "pickup":
            message = (
                f"Warehouse notified for Order #{order.order_id} — ready for pickup."
            )
            print(f"{blue_blink}{message}{reset}")
