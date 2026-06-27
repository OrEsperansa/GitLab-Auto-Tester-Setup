from ticket import Ticket


class RegularTicket(Ticket):
    def calculate_price(self):
        return 50
