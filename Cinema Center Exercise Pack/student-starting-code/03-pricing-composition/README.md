# Exercise 3 - Inheritance Starts Becoming a Trap

## Existing system

You have ticket subclasses for regular, student, senior, and VIP tickets.

## New business requirement

The cinema introduces memberships, weekend pricing, holiday pricing, promo codes, and stackable discounts.

## Pain caused by the old design

Trying to model every combination with inheritance creates classes like `WeekendVipTicket` and `StudentPremiumTicket`.

## Refactor requirement

Keep ticket subclasses for the stable ticket types. Move changing price rules into separate policy objects that can be attached and combined.

Required files:

- `ticket.py`
- `tickets.py`
- `pricing.py`
- `customer.py`
