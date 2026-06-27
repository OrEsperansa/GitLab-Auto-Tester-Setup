import inspect

import pytest


def test_ticket_is_abstract_and_subclasses_inherit(load_module):
    Ticket = load_module("ticket").Ticket
    RegularTicket = load_module("regular_ticket").RegularTicket
    StudentTicket = load_module("student_ticket").StudentTicket
    SeniorTicket = load_module("senior_ticket").SeniorTicket
    VipTicket = load_module("vip_ticket").VipTicket

    assert inspect.isabstract(Ticket), "Ticket should be an abstract base class now."
    assert issubclass(RegularTicket, Ticket)
    assert issubclass(StudentTicket, Ticket)
    assert issubclass(SeniorTicket, Ticket)
    assert issubclass(VipTicket, Ticket)


def test_ticket_types_calculate_and_validate_their_own_rules(load_module):
    Seat = load_module("seat").Seat
    Screening = load_module("screening").Screening
    RegularTicket = load_module("regular_ticket").RegularTicket
    StudentTicket = load_module("student_ticket").StudentTicket
    SeniorTicket = load_module("senior_ticket").SeniorTicket
    VipTicket = load_module("vip_ticket").VipTicket

    screening = Screening("Dune", [Seat("A", 1), Seat("A", 2, is_vip=True)])

    assert RegularTicket("Ari", screening, screening.get_seat("A1")).price == 50
    assert StudentTicket("Dana", screening, screening.get_seat("A1"), "S-123").price == 35
    assert SeniorTicket("Ruth", screening, screening.get_seat("A1")).price == 30
    assert VipTicket("Sam", screening, screening.get_seat("A2")).price == 90

    with pytest.raises(ValueError):
        StudentTicket("Dana", screening, screening.get_seat("A1"), "")

    with pytest.raises(ValueError):
        VipTicket("Sam", screening, screening.get_seat("A1"))


def test_cinema_sells_polymorphic_ticket_without_type_chain(load_module):
    Seat = load_module("seat").Seat
    Screening = load_module("screening").Screening
    CinemaCenter = load_module("cinema_center").CinemaCenter
    RegularTicket = load_module("regular_ticket").RegularTicket
    cinema_source = inspect.getsource(CinemaCenter)

    assert "ticket_type" not in cinema_source
    assert "isinstance" not in cinema_source

    screening = Screening("Soul", [Seat("B", 1)])
    ticket = RegularTicket("Maya", screening, screening.get_seat("B1"))
    sold = CinemaCenter().sell_ticket(ticket)

    assert sold is ticket
    assert "B1" in screening.sold_seat_codes

    with pytest.raises(ValueError):
        CinemaCenter().sell_ticket(ticket)
