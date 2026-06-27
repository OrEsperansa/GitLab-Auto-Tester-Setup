class Seat:
    def __init__(self, row, number):
        self.row = row
        self.number = number

    @property
    def code(self):
        return f"{self.row}{self.number}"
