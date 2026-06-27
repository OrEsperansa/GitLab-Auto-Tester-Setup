# Exercise 1 - The First Working Cinema System

## Existing system

You are starting a new cinema center application.

## New business requirement

The cinema has one branch and sells only regular tickets.

## Pain caused by the old design

There is no old design yet. Keep the design simple because there is only one ticket type.

## Refactor requirement

Build normal concrete classes. Do not create abstract ticket classes yet.

Required files and classes:

- `movie.py` - `Movie`
- `seat.py` - `Seat`
- `auditorium.py` - `Auditorium`
- `screening.py` - `Screening`
- `ticket.py` - `Ticket`
- `cinema_center.py` - `CinemaCenter`

The system must add movies and auditoriums, create screenings, sell one regular ticket for one seat, prevent selling the same seat twice for the same screening, and store customer name, screening, seat, and price on the ticket.
