class BookingConfirmed:
    def __init__(self, booking):
        self.booking = booking


class ScreeningCancelled:
    def __init__(self, screening):
        self.screening = screening


class EventBus:
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        self.listeners.append(listener)

    def publish(self, event):
        for listener in self.listeners:
            listener.handle(event)
