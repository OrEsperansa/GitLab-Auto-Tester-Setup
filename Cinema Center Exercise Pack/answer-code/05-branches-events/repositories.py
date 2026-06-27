class InMemoryRepository:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
        return item

    def all(self):
        return list(self.items)
