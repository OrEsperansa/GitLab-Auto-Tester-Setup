def test_solution_is_split_into_expected_modules(load_module):
    animal_module = load_module("animal")
    dog_module = load_module("dog")
    cat_module = load_module("cat")
    summary_module = load_module("summary")

    assert hasattr(animal_module, "Animal")
    assert hasattr(dog_module, "Dog")
    assert hasattr(cat_module, "Cat")
    assert hasattr(summary_module, "create_animal_summary")


def test_dog_and_cat_inherit_from_animal(load_module):
    animal_module = load_module("animal")
    dog_module = load_module("dog")
    cat_module = load_module("cat")

    assert issubclass(dog_module.Dog, animal_module.Animal)
    assert issubclass(cat_module.Cat, animal_module.Animal)
