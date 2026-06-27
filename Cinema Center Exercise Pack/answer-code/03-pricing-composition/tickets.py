from ticket import Ticket


class RegularTicket(Ticket):
    def __init__(self, customer):
        super().__init__(customer, 50)


class StudentTicket(Ticket):
    def __init__(self, customer, student_id):
        if not student_id:
            raise ValueError("student ticket requires a student id")
        self.student_id = student_id
        super().__init__(customer, 35)


class VipTicket(Ticket):
    def __init__(self, customer, seat_is_vip=True):
        if not seat_is_vip:
            raise ValueError("VIP ticket requires a VIP seat")
        self.lounge_access = True
        super().__init__(customer, 90)
