def test_dog_has_own_sound_and_description(load_module):
    dog_module = load_module("dog")
    dog = dog_module.Dog("Rex", "Labrador")

    assert dog.speak() == "Rex says woof!"
    assert dog.describe() == "Rex is a dog with 50 energy. Breed: Labrador."


def test_cat_has_own_sound_and_description(load_module):
    cat_module = load_module("cat")
    cat = cat_module.Cat("Luna", indoor=False)

    assert cat.speak() == "Luna says meow!"
    assert cat.describe() == "Luna is a cat with 50 energy. Outdoor cat."
