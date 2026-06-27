from ticket import Ticket


class SeniorTicket(Ticket):
    def calculate_price(self):
        return 30
