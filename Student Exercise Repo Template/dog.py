from animal import Animal


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "dog")
        self.breed = breed

    def speak(self):
        return f"{self.name} says woof!"

    def describe(self):
        base_description = super().describe()
        return f"{base_description} Breed: {self.breed}."
