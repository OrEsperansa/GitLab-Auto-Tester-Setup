from events import BookingConfirmed, ScreeningCancelled


class NotificationListener:
    def __init__(self):
        self.messages = []

    def handle(self, event):
        if isinstance(event, BookingConfirmed):
            self.messages.append(f"Booking confirmed for {event.booking.customer_name}")
        if isinstance(event, ScreeningCancelled):
            self.messages.append("Screening cancelled")


class RevenueReportListener:
    def __init__(self):
        self.revenue = 0

    def handle(self, event):
        if isinstance(event, BookingConfirmed):
            self.revenue += event.booking.total_price


class WaitlistListener:
    def __init__(self):
        self.released_screenings = []

    def handle(self, event):
        if isinstance(event, ScreeningCancelled):
            self.released_screenings.append(event.screening)
