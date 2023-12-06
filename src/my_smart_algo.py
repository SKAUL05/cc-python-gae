import random
import math
import json
from config import _TEAM


def apply_guess(*args, **kwargs):

    my_guess = {"guesses": []}

    if dead_participants_index := [
        index
        for index in range(len(kwargs.get("participants", 0)))
        if (
            not kwargs.get("participants", {})[index]["isAlive"]
            or kwargs.get("participants", {})[index]["name"] == _TEAM.upper()
        )
    ]:
        for index in sorted(dead_participants_index, reverse=True):
            del kwargs["participants"][index]

    total_participants = len(kwargs["participants"])

    for _ in range(5):
        try:
            participant = kwargs["participants"][
                random.randint(0, total_participants - 1)
            ]
            secret_range = math.pow(10, kwargs["secret_length"] - 1)
            secret = random.randint(secret_range, secret_range * 10 - 1)
            guess = {"team": participant["name"], "guess": str(secret)}
            my_guess["guesses"].append(guess)

        except Exception as e:
            print(e)
            return None

    return my_guess
