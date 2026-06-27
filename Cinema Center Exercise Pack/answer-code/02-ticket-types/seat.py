class Seat:
    def __init__(self, row, number, is_vip=False):
        self.row = row
        self.number = number
        self.is_vip = is_vip

    @property
    def code(self):
        return f"{self.row}{self.number}"
