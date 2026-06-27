from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount):
        raise NotImplementedError


class CardPaymentProcessor(PaymentProcessor):
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed

    def charge(self, amount):
        return self.should_succeed


class CashPaymentProcessor(PaymentProcessor):
    def charge(self, amount):
        return True


class WalletPaymentProcessor(PaymentProcessor):
    def __init__(self, balance):
        self.balance = balance

    def charge(self, amount):
        if self.balance < amount:
            return False
        self.balance -= amount
        return True
