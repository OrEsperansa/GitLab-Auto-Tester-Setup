def test_create_animal_summary_uses_polymorphism(load_module):
    dog_module = load_module("dog")
    cat_module = load_module("cat")
    summary_module = load_module("summary")
    animals = [
        dog_module.Dog("Rex", "Labrador"),
        cat_module.Cat("Luna", indoor=True),
    ]

    assert summary_module.create_animal_summary(animals) == [
        "Rex says woof!",
        "Luna says meow!",
    ]
