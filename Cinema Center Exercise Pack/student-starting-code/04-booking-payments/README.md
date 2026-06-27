# Exercise 4 - Payments Turn CinemaCenter Into a God Class

## Existing system

You have tickets and pricing rules.

## New business requirement

The cinema supports reservations, payment failures, cash/card/wallet payments, refunds, and reservation expiry after 15 minutes.

## Pain caused by the old design

Putting reservation state, pricing, payment, refunds, seat release, and confirmations inside one class creates a giant class with too many responsibilities.

## Refactor requirement

Introduce focused objects:

- `Booking`
- `CheckoutService`
- `PaymentProcessor`
- `CardPaymentProcessor`
- `CashPaymentProcessor`
- `WalletPaymentProcessor`
- `RefundPolicy`
