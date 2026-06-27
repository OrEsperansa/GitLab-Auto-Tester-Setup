# Cinema Center Exercise Pack

This folder contains the full rolling OOP refactor exercise series.

## Folder layout

- `student-starting-code/` - the code students receive at the start of each exercise
- `answer-code/` - reference implementations for teachers
- `hidden-tests/` - pytest tests for automatic checking

## Exercises

1. `01-first-working-system` - build the first concrete cinema system
2. `02-ticket-types` - refactor tickets into an abstract base class with subclasses
3. `03-pricing-composition` - move changing price rules into composable policies
4. `04-booking-payments` - separate booking state, checkout flow, payments, and refunds
5. `05-branches-events` - introduce branches, repositories, domain events, and listeners

The teaching idea is that Exercise 1 is not "bad architecture." It is the simplest correct design for the requirements at the time. Each later exercise adds pressure that makes a refactor feel necessary.
