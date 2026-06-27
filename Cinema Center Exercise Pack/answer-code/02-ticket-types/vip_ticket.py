from ticket import Ticket


class VipTicket(Ticket):
    lounge_access = True

    def calculate_price(self):
        return 90

    def validate(self):
        if not self.seat.is_vip:
            raise ValueError("VIP tickets can only be sold for VIP seats")
