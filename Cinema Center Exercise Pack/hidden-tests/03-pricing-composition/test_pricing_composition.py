import inspect


def test_ticket_types_keep_only_core_behavior(load_module):
    Customer = load_module("customer").Customer
    tickets = load_module("tickets")

    customer = Customer("Maya", membership="premium")
    regular = tickets.RegularTicket(customer)
    student = tickets.StudentTicket(customer, "S-9")
    vip = tickets.VipTicket(customer, seat_is_vip=True)

    assert regular.calculate_base_price() == 50
    assert student.calculate_base_price() == 35
    assert vip.calculate_base_price() == 90
    assert vip.lounge_access is True


def test_pricing_policies_can_be_combined_in_order(load_module):
    Customer = load_module("customer").Customer
    RegularTicket = load_module("tickets").RegularTicket
    pricing = load_module("pricing")

    ticket = RegularTicket(Customer("Noa", membership="premium"))
    calculator = pricing.PricingCalculator([
        pricing.WeekendSurcharge(),
        pricing.MembershipDiscount(),
        pricing.PromoCodeDiscount("SAVE10"),
    ])

    assert calculator.final_price(ticket) == 38


def test_new_policy_can_be_added_without_editing_ticket_classes(load_module):
    Customer = load_module("customer").Customer
    VipTicket = load_module("tickets").VipTicket
    PricingPolicy = load_module("pricing").PricingPolicy
    PricingCalculator = load_module("pricing").PricingCalculator
    ticket_source = inspect.getsource(load_module("tickets"))

    class TuesdayDiscount(PricingPolicy):
        def apply(self, price, ticket):
            return price * 0.8

    ticket = VipTicket(Customer("Ari", membership="basic"), seat_is_vip=True)
    calculator = PricingCalculator([TuesdayDiscount()])

    assert calculator.final_price(ticket) == 72
    assert "TuesdayDiscount" not in ticket_source
    assert "WeekendVipTicket" not in ticket_source
    assert "StudentPremiumTicket" not in ticket_source
