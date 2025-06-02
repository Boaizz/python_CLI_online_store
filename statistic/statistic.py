from datetime import date

class Statistic:
    def __init__(self):
        self.daily_sales: dict[date, dict[int,int]] = {}

    def record_order(self, order):
        d = order.created_at.date()
        if d not in self.daily_sales:
            self.daily_sales[d] = {}
        for oi in order.order_items:
            pid = oi.product.product_id
            self.daily_sales[d][pid] = (
                self.daily_sales[d].get(pid, 0) + oi.qty
            )

    def report(self, d: date):
        print(f"\nSales Report for {d.isoformat()}:")
        day = self.daily_sales.get(d, {})
        if not day:
            print("No sales recorded today!")
            return
        for pid, qty in day.items():
            print(f"  Product {pid}: {qty} unit(s) sold.")
        print()