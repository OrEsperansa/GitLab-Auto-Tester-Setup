class FakeBooking:
    def __init__(self, customer_name, screening, total_price):
        self.customer_name = customer_name
        self.screening = screening
        self.total_price = total_price
        self.status = "reserved"
        self.refunded = False

    def confirm(self):
        self.status = "confirmed"

    def refund(self):
        self.status = "refunded"
        self.refunded = True


class FakeScreening:
    cancelled = False


def test_branch_keeps_its_own_auditoriums_and_screenings(load_module):
    CinemaBranch = load_module("branch").CinemaBranch

    north = CinemaBranch("North")
    south = CinemaBranch("South")
    north.add_auditorium("North Hall")
    south.add_auditorium("South Hall")
    north.add_screening("North Screening")

    assert north.auditoriums == ["North Hall"]
    assert south.auditoriums == ["South Hall"]
    assert north.screenings == ["North Screening"]
    assert south.screenings == []


def test_confirm_booking_publishes_events_to_listeners(load_module):
    EventBus = load_module("events").EventBus
    InMemoryRepository = load_module("repositories").InMemoryRepository
    CinemaSystem = load_module("cinema_system").CinemaSystem
    NotificationListener = load_module("listeners").NotificationListener
    RevenueReportListener = load_module("listeners").RevenueReportListener

    bus = EventBus()
    notifications = NotificationListener()
    revenue = RevenueReportListener()
    bus.subscribe(notifications)
    bus.subscribe(revenue)

    booking = FakeBooking("Maya", FakeScreening(), 120)
    system = CinemaSystem(bus, InMemoryRepository())
    system.confirm_booking(booking)

    assert booking.status == "confirmed"
    assert notifications.messages == ["Booking confirmed for Maya"]
    assert revenue.revenue == 120


def test_screening_cancellation_refunds_and_notifies_without_direct_listener_calls(load_module):
    EventBus = load_module("events").EventBus
    InMemoryRepository = load_module("repositories").InMemoryRepository
    CinemaSystem = load_module("cinema_system").CinemaSystem
    NotificationListener = load_module("listeners").NotificationListener
    WaitlistListener = load_module("listeners").WaitlistListener

    bus = EventBus()
    notifications = NotificationListener()
    waitlist = WaitlistListener()
    bus.subscribe(notifications)
    bus.subscribe(waitlist)

    repository = InMemoryRepository()
    screening = FakeScreening()
    booking = FakeBooking("Noa", screening, 50)
    booking.confirm()
    repository.add(booking)

    system = CinemaSystem(bus, repository)
    system.cancel_screening(screening)

    assert screening.cancelled is True
    assert booking.refunded is True
    assert notifications.messages == ["Screening cancelled"]
    assert waitlist.released_screenings == [screening]
