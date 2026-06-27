class Ticket:
    def __init__(self, customer, base_price):
        self.customer = customer
        self.base_price = base_price

    def calculate_base_price(self):
        return self.base_price
