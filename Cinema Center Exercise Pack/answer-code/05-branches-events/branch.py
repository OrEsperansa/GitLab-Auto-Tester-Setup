class CinemaBranch:
    def __init__(self, name):
        self.name = name
        self.auditoriums = []
        self.screenings = []

    def add_auditorium(self, auditorium):
        self.auditoriums.append(auditorium)

    def add_screening(self, screening):
        self.screenings.append(screening)
