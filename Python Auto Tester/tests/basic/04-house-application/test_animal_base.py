import pytest


def test_animal_base_class_tracks_name_and_species(load_module):
    animal_module = load_module("animal")
    animal = animal_module.Animal("Milo", "unknown")

    assert animal.name == "Milo"
    assert animal.species == "unknown"
    assert animal.energy == 50
    assert animal.describe() == "Milo is a unknown with 50 energy."


def test_feed_increases_energy_but_not_above_100(load_module):
    dog_module = load_module("dog")
    dog = dog_module.Dog("Rex", "Labrador")

    dog.feed(30)
    assert dog.energy == 80

    dog.feed(50)
    assert dog.energy == 100


def test_play_decreases_energy_and_returns_activity_message(load_module):
    cat_module = load_module("cat")
    cat = cat_module.Cat("Luna", indoor=True)

    assert cat.play(20) == "Luna plays happily."
    assert cat.energy == 30


def test_play_refuses_when_energy_is_too_low(load_module):
    dog_module = load_module("dog")
    dog = dog_module.Dog("Rex", "Labrador")

    dog.play(45)

    with pytest.raises(ValueError):
        dog.play(10)
