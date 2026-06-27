from datetime import timedelta


class RefundPolicy:
    def refund_amount(self, booking, now):
        if booking.screening.starts_at - now >= timedelta(hours=24):
            return booking.total_price
        if booking.screening.starts_at - now >= timedelta(hours=2):
            return booking.total_price * 0.5
        return 0
