class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.energy = 50

    def feed(self, amount):
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.energy = min(100, self.energy + amount)

    def play(self, cost):
        if cost < 0:
            raise ValueError("cost must be non-negative")
        if self.energy < cost:
            raise ValueError(f"{self.name} is too tired to play.")
        self.energy -= cost
        return f"{self.name} plays happily."

    def speak(self):
        return f"{self.name} makes a sound."

    def describe(self):
        return f"{self.name} is a {self.species} with {self.energy} energy."
