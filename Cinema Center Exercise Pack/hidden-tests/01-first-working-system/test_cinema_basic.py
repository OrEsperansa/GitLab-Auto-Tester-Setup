import pytest


def test_expected_classes_exist(load_module):
    assert hasattr(load_module("movie"), "Movie")
    assert hasattr(load_module("seat"), "Seat")
    assert hasattr(load_module("auditorium"), "Auditorium")
    assert hasattr(load_module("screening"), "Screening")
    assert hasattr(load_module("ticket"), "Ticket")
    assert hasattr(load_module("cinema_center"), "CinemaCenter")


def test_can_create_screening_and_sell_regular_ticket(load_module):
    Movie = load_module("movie").Movie
    Auditorium = load_module("auditorium").Auditorium
    CinemaCenter = load_module("cinema_center").CinemaCenter

    cinema = CinemaCenter("Downtown Cinema")
    movie = Movie("Hidden Figures", 127)
    auditorium = Auditorium("Hall 1", rows=2, seats_per_row=3)

    cinema.add_movie(movie)
    cinema.add_auditorium(auditorium)
    screening = cinema.create_screening(movie, auditorium, "2026-07-01 20:00")
    ticket = cinema.sell_ticket("Maya", screening, "A1")

    assert ticket.customer_name == "Maya"
    assert ticket.screening is screening
    assert ticket.seat.code == "A1"
    assert ticket.price > 0
    assert ticket.ticket_type == "regular"


def test_same_seat_cannot_be_sold_twice_for_same_screening(load_module):
    Movie = load_module("movie").Movie
    Auditorium = load_module("auditorium").Auditorium
    CinemaCenter = load_module("cinema_center").CinemaCenter

    cinema = CinemaCenter("Downtown Cinema")
    movie = Movie("Arrival", 116)
    auditorium = Auditorium("Hall 2", rows=1, seats_per_row=2)
    cinema.add_movie(movie)
    cinema.add_auditorium(auditorium)
    screening = cinema.create_screening(movie, auditorium, "2026-07-02 18:00")

    cinema.sell_ticket("Noam", screening, "A1")

    with pytest.raises(ValueError):
        cinema.sell_ticket("Lior", screening, "A1")
