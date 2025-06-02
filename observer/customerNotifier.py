from observer.observer import Observer
from order.order import Order

class CustomerNotifier(Observer):
    def update(self, order: Order, event: str):
        yellow_blink = "\033[5;93m"  
        reset = "\033[0m"
        message = (
            f"Notification to {order.customer.name}: "
            f"Your order #{order.order_id} status is changed to {event}!"
        )
        print(f"{yellow_blink}{message}{reset}")