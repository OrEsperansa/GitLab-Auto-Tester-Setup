from animal import Animal


class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, "cat")
        self.indoor = indoor

    def speak(self):
        return f"{self.name} says meow!"

    def describe(self):
        base_description = super().describe()
        lifestyle = "Indoor cat" if self.indoor else "Outdoor cat"
        return f"{base_description} {lifestyle}."
