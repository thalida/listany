import random

from django.contrib.auth.models import Group

USERNAME_COLORS = [
    "Red",
    "Orange",
    "Yellow",
    "Green",
    "Blue",
    "Purple",
    "Pink",
    "Brown",
    "Black",
    "White",
    "Gray",
    "Silver",
    "Gold",
    "Beige",
    "Turquoise",
    "Magenta",
    "Indigo",
    "Lavender",
    "Maroon",
    "Navy",
    "Teal",
    "Olive",
    "Coral",
    "Salmon",
    "Fuchsia",
    "Khaki",
    "Plum",
    "Tan",
    "Sky Blue",
    "Mint Green",
]

USERNAME_MYTICAL_ANIMALS = [
    "Dragon",
    "Unicorn",
    "Phoenix",
    "Yeti",
    "Cyclops",
    "Sphinx",
    "Cerberus",
    "Pegasus",
    "Centaur",
    "Bigfoot",
    "Nessie",
]


def get_username(strategy, details, user=None, *args, **kwargs):
    storage = strategy.storage

    if user:
        return {"username": storage.user.get_username(user)}

    rand_color = random.choice(USERNAME_COLORS)
    rand_animal = random.choice(USERNAME_MYTICAL_ANIMALS)
    details["username"] = f"{rand_color}_{rand_animal}"

    return details


def assign_default_groups(backend, user, response, *args, **kwargs):
    basic_user_group = Group.objects.get(name="basic_user")
    basic_user_group.user_set.add(user)
