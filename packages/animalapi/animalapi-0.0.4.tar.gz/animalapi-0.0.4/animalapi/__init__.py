import random
import requests

BASE_URL = "https://some-random-api.ml/"
VALID_ANIMALS = [
    "dog",
    "cat",
    "bird",
    "koala",
]

class InvalidAnimalError(ValueError):
    """Raised when an invalid animal name is provided."""

    pass


def animal_data(animal_name):
    if animal_name not in VALID_ANIMALS:
        raise InvalidAnimalError(
            f"Invalid animal name: {animal_name}. Valid animals are: {', '.join(VALID_ANIMALS)}"
        )

    res = requests.get(BASE_URL + f"animal/{animal_name}")

    if res.status_code != 200:
        raise requests.exceptions.RequestException(
            f"API request failed with status code {res.status_code}: {res.text}"
        )

    try:
        return res.json()
    except ValueError:
        raise ValueError("Invalid JSON response from API")


def rand_animals():
    random_animal = random.choice(VALID_ANIMALS)
    return animal_data(random_animal)
