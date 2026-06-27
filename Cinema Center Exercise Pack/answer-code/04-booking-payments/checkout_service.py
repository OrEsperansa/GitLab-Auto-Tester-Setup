class CheckoutService:
    def __init__(self, payment_processor):
        self.payment_processor = payment_processor

    def checkout(self, booking):
        if self.payment_processor.charge(booking.total_price):
            booking.confirm()
            return True
        booking.release()
        return False

    def expire_reservation(self, booking, now):
        if booking.is_expired(now):
            booking.release()
            return True
        return False
