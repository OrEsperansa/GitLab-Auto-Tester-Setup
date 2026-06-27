from screening import Screening
from ticket import Ticket


class CinemaCenter:
    def __init__(self, name):
        self.name = name
        self.movies = []
        self.auditoriums = []
        self.screenings = []
        self.tickets = []

    def add_movie(self, movie):
        self.movies.append(movie)

    def add_auditorium(self, auditorium):
        self.auditoriums.append(auditorium)

    def create_screening(self, movie, auditorium, starts_at):
        if movie not in self.movies:
            raise ValueError("movie must be added before creating a screening")
        if auditorium not in self.auditoriums:
            raise ValueError("auditorium must be added before creating a screening")
        screening = Screening(movie, auditorium, starts_at)
        self.screenings.append(screening)
        return screening

    def sell_ticket(self, customer_name, screening, seat_code, price=50):
        seat = screening.auditorium.find_seat(seat_code)
        if seat.code in screening.sold_seat_codes:
            raise ValueError("seat is already sold for this screening")
        ticket = Ticket(customer_name, screening, seat, price)
        screening.sold_seat_codes.add(seat.code)
        self.tickets.append(ticket)
        return ticket
