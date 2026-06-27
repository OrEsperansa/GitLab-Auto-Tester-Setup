class CinemaCenter:
    def __init__(self):
        self.tickets = []

    def sell_ticket(self, ticket):
        seat_code = ticket.seat.code
        if seat_code in ticket.screening.sold_seat_codes:
            raise ValueError("seat is already sold for this screening")
        ticket.screening.sold_seat_codes.add(seat_code)
        self.tickets.append(ticket)
        return ticket
