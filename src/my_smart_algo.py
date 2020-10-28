import random
import math
import json
import logging
from utils import logger_initialise

logger_initialise()


def apply_guess(game_id, round_id, secret_length, participants, tracker):
    logging.info("In Apply Guess")
    my_guess = {"guesses": []}
    secret_length = 1 if not secret_length else secret_length
    # Remove myself, I don't want to guess my secret and eventually suicide. Do I? :)
    # Also remove "dead" enemies
    dead_participants_index = []
    for index in range(len(participants)):
        if (
            not participants[index]["isAlive"]
            or participants[index]["teamId"].upper() == _TEAM.upper()
        ):
            dead_participants_index.append(index)

    if len(dead_participants_index) > 0:
        for index in sorted(dead_participants_index, reverse=True):
            del participants[index]

    total_participants = len(participants)

    for random_guess in range(5):
        try:
            participant = participants[random.randint(0, total_participants - 1)]
            secret_range = math.pow(10, secret_length - 1)
            secret = random.randint(secret_range, secret_range * 10 - 1)
            guess = {}
            guess["team"] = participant["teamId"]
            guess["guess"] = str(secret)
            my_guess["guesses"].append(guess)

        except Exception as e:
            logging.error(e)
            return None

    return my_guess
