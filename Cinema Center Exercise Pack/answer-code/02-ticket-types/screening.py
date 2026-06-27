class Screening:
    def __init__(self, movie_title, seats):
        self.movie_title = movie_title
        self.seats = {seat.code: seat for seat in seats}
        self.sold_seat_codes = set()

    def get_seat(self, seat_code):
        try:
            return self.seats[seat_code]
        except KeyError as exc:
            raise ValueError("seat does not exist") from exc
