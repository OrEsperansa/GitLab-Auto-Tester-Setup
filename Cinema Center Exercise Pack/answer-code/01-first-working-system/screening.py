class Screening:
    def __init__(self, movie, auditorium, starts_at):
        self.movie = movie
        self.auditorium = auditorium
        self.starts_at = starts_at
        self.sold_seat_codes = set()
