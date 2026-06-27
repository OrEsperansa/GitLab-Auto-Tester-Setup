from datetime import timedelta


class Booking:
    RESERVED = "reserved"
    CONFIRMED = "confirmed"
    RELEASED = "released"
    REFUNDED = "refunded"

    def __init__(self, customer_name, screening, seats, total_price, reserved_at):
        self.customer_name = customer_name
        self.screening = screening
        self.seats = seats
        self.total_price = total_price
        self.reserved_at = reserved_at
        self.status = self.RESERVED
        for seat in seats:
            screening.reserve_seat(seat)

    def confirm(self):
        self.status = self.CONFIRMED

    def release(self):
        for seat in self.seats:
            self.screening.release_seat(seat)
        self.status = self.RELEASED

    def mark_refunded(self):
        self.status = self.REFUNDED

    def is_expired(self, now):
        return self.status == self.RESERVED and now - self.reserved_at > timedelta(minutes=15)
