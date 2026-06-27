from datetime import datetime, timedelta


class FakeScreening:
    def __init__(self, starts_at=None):
        self.starts_at = starts_at or datetime(2026, 7, 10, 20, 0)
        self.reserved = set()

    def reserve_seat(self, seat):
        if seat in self.reserved:
            raise ValueError("seat already reserved")
        self.reserved.add(seat)

    def release_seat(self, seat):
        self.reserved.discard(seat)


def test_successful_checkout_confirms_booking(load_module):
    Booking = load_module("booking").Booking
    CheckoutService = load_module("checkout_service").CheckoutService
    CashPaymentProcessor = load_module("payments").CashPaymentProcessor

    screening = FakeScreening()
    booking = Booking("Maya", screening, ["A1"], 50, datetime(2026, 7, 1, 12, 0))
    result = CheckoutService(CashPaymentProcessor()).checkout(booking)

    assert result is True
    assert booking.status == "confirmed"
    assert "A1" in screening.reserved


def test_failed_payment_releases_reserved_seats(load_module):
    Booking = load_module("booking").Booking
    CheckoutService = load_module("checkout_service").CheckoutService
    CardPaymentProcessor = load_module("payments").CardPaymentProcessor

    screening = FakeScreening()
    booking = Booking("Noam", screening, ["B1", "B2"], 100, datetime(2026, 7, 1, 12, 0))
    result = CheckoutService(CardPaymentProcessor(should_succeed=False)).checkout(booking)

    assert result is False
    assert booking.status == "released"
    assert screening.reserved == set()


def test_expired_reservation_releases_seats(load_module):
    Booking = load_module("booking").Booking
    CheckoutService = load_module("checkout_service").CheckoutService
    CashPaymentProcessor = load_module("payments").CashPaymentProcessor

    screening = FakeScreening()
    reserved_at = datetime(2026, 7, 1, 12, 0)
    booking = Booking("Lior", screening, ["C1"], 50, reserved_at)

    expired = CheckoutService(CashPaymentProcessor()).expire_reservation(
        booking,
        reserved_at + timedelta(minutes=16),
    )

    assert expired is True
    assert booking.status == "released"
    assert "C1" not in screening.reserved


def test_refund_policy_depends_on_time_before_screening(load_module):
    Booking = load_module("booking").Booking
    RefundPolicy = load_module("refund_policy").RefundPolicy
    starts_at = datetime(2026, 7, 10, 20, 0)
    booking = Booking("Dana", FakeScreening(starts_at), ["D1"], 80, datetime(2026, 7, 1, 12, 0))
    policy = RefundPolicy()

    assert policy.refund_amount(booking, starts_at - timedelta(days=2)) == 80
    assert policy.refund_amount(booking, starts_at - timedelta(hours=3)) == 40
    assert policy.refund_amount(booking, starts_at - timedelta(hours=1)) == 0
