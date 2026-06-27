from events import BookingConfirmed, ScreeningCancelled


class CinemaSystem:
    def __init__(self, event_bus, booking_repository):
        self.event_bus = event_bus
        self.booking_repository = booking_repository

    def confirm_booking(self, booking):
        booking.confirm()
        self.booking_repository.add(booking)
        self.event_bus.publish(BookingConfirmed(booking))

    def cancel_screening(self, screening):
        screening.cancelled = True
        for booking in self.booking_repository.all():
            if booking.screening is screening and booking.status == "confirmed":
                booking.refund()
        self.event_bus.publish(ScreeningCancelled(screening))
