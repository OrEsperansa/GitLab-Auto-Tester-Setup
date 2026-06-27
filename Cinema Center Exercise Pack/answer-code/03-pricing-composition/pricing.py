from abc import ABC, abstractmethod


class PricingPolicy(ABC):
    @abstractmethod
    def apply(self, price, ticket):
        raise NotImplementedError


class WeekendSurcharge(PricingPolicy):
    def apply(self, price, ticket):
        return price + 10


class MembershipDiscount(PricingPolicy):
    discounts = {"basic": 0, "plus": 0.10, "premium": 0.20}

    def apply(self, price, ticket):
        discount = self.discounts.get(ticket.customer.membership, 0)
        return price * (1 - discount)


class PromoCodeDiscount(PricingPolicy):
    def __init__(self, code):
        self.code = code

    def apply(self, price, ticket):
        if self.code == "SAVE10":
            return price - 10
        return price


class PricingCalculator:
    def __init__(self, policies=None):
        self.policies = list(policies or [])

    def add_policy(self, policy):
        self.policies.append(policy)

    def final_price(self, ticket):
        price = ticket.calculate_base_price()
        for policy in self.policies:
            price = policy.apply(price, ticket)
        return max(round(price, 2), 0)
