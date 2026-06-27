# Exercise 2 - Ticket Types Break the Original Design

## Existing system

You already have a working cinema that sells regular tickets.

## New business requirement

The cinema now sells regular, student, senior, and VIP tickets.

## Pain caused by the old design

A single concrete `Ticket` class would start collecting ticket-type checks, special fields, and mixed validation rules.

## Refactor requirement

Turn `Ticket` into an abstract base class and create concrete ticket classes:

- `RegularTicket`
- `StudentTicket`
- `SeniorTicket`
- `VipTicket`

Each ticket type must calculate its own price and validate its own rules. The cinema system must work with ticket objects without checking their exact type.
