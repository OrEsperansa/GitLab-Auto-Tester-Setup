class Ticket:
    def __init__(self, customer_name, screening, seat, price=50):
        self.customer_name = customer_name
        self.screening = screening
        self.seat = seat
        self.price = price
        self.ticket_type = "regular"
