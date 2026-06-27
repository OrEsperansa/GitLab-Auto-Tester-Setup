from seat import Seat


class Auditorium:
    def __init__(self, name, rows=3, seats_per_row=5):
        self.name = name
        self.seats = [
            Seat(chr(65 + row_index), number)
            for row_index in range(rows)
            for number in range(1, seats_per_row + 1)
        ]

    def find_seat(self, seat_code):
        for seat in self.seats:
            if seat.code == seat_code:
                return seat
        raise ValueError("seat does not exist in this auditorium")
