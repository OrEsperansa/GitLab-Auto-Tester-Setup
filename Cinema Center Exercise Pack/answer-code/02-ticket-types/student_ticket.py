from ticket import Ticket


class StudentTicket(Ticket):
    def __init__(self, customer_name, screening, seat, student_id):
        self.student_id = student_id
        super().__init__(customer_name, screening, seat)

    def calculate_price(self):
        return 35

    def validate(self):
        if not self.student_id:
            raise ValueError("student ticket requires a valid student id")
