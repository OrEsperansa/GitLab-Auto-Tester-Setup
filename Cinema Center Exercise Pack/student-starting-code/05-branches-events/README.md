# Exercise 5 - Multi-Branch Scale, Events, and Extensibility

## Existing system

You have bookings, payments, and reservation workflows.

## New business requirement

The business expands into multiple branches and needs reports, cancellation workflows, notifications, waitlists, and future storage integrations.

## Pain caused by the old design

Directly sending emails, updating reports, storing everything in domain classes, and calling every affected feature from core logic makes the system tightly coupled.

## Refactor requirement

Introduce branches, repositories, domain events, and listeners. Core business logic should publish that something happened; other objects decide how to react.
