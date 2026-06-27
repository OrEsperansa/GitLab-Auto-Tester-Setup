from abc import ABC, abstractmethod


class Ticket(ABC):
    def __init__(self, customer_name, screening, seat):
        self.customer_name = customer_name
        self.screening = screening
        self.seat = seat
        self.price = self.calculate_price()
        self.validate()

    @abstractmethod
    def calculate_price(self):
        raise NotImplementedError

    def validate(self):
        return None
