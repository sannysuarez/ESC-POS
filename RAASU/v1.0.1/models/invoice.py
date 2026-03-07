class Invoice:
    def __init__(self, invoice_no, customer_name, items, total, cashier):
        """
        items: list of dicts, each like {'name': 'Item1', 'qty': 2, 'unit_price': 150}
        """
        self.invoice_no = invoice_no
        self.customer_name = customer_name
        self.items = items
        self.total = total
        self.cashier = cashier

    def to_dict(self):
        return {
            "invoice_no": self.invoice_no,
            "customer_name": self.customer_name,
            "items": self.items,
            "total": self.total,
            "cashier": self.cashier
        }