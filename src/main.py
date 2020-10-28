import os
import time
import json
import google.cloud.logging
import logging
from flask import Flask, render_template
from config import _TEAM
from game_api import get_game_status, join_game, make_guess
from my_smart_algo import apply_guess
from colorama import init, Fore, Style
from utils import create_task

app = Flask(__name__)
_MY_GUESS_TRACKER = {}
_TEAM_NOT_PROVIDED = (
    "Please put your team name and password into config.py and start again."
)
# logging.getLogger().setLevel(logging.INFO)

client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()


def game_status_received(err, data):
    if err is not None:
        logging.error(err)
        logging.error("Get Game Status Failed")
    else:
        logging.info(
            "GameId: {}\n RoundId: {}\n State: {}\n #Participants: {}".format(
                data["gameId"],
                data["roundId"],
                data["status"],
                len(data["participants"]),
            )
        )
        logging.info(
            "------------------------------------------------------------------------------------------\n"
        )
        state = data["status"]
        key = str(data["gameId"]) + "-" + str(data["roundId"])
        joined_status = False
        alive_status = False
        team_name = _TEAM.upper()
        for participant in data["participants"]:
            logging.info(team_name)
            logging.info(participant)
            participant_id = participant.get("teamId","").upper()
            logging.info("Participant Id {}".format(participant_id))
            if (
                participant_id == team_name
                # and participant["joinedInThisRound"] == True
            ):
                joined_status = True
                alive_status = participant["isAlive"]

        if state.lower() == "joining":

            if not joined_status:
                err_join, data_join = join_game()
                if err_join is not None:
                    logging.error("Join Failed")
                    logging.error(err_join)
                else:
                    logging.info("Join Successful")
                    logging.info(data_join["message"])

            else:
                logging.info("Already joined, waiting to play...")

        elif state.lower() == "running":
            if not joined_status:
                logging.info(
                    "Oho, I have missed the joining phase, let me wait till the next round starts"
                )
            elif not alive_status:
                logging.error("I am dead, waiting to respawn in next round...:(")
            else:
                my_next_guess = apply_guess(
                    data["gameId"],
                    data["roundId"],
                    data["secretLength"],
                    data["participants"],
                    _MY_GUESS_TRACKER,
                )
                if my_next_guess is not None and len(my_next_guess["guesses"]) > 0:
                    logging.info(my_next_guess)
                    json_object = json.dumps(my_next_guess)
                    err_guess, data_guess = make_guess(json_object)

                    if err_guess is not None:
                        logging.error("Guess Failed\n")
                        logging.error(err_guess, "\n")

                    else:
                        total_score_current_guess = 0
                        if (
                            "guesses" in data_guess
                            and data_guess["guesses"] is not None
                        ):
                            for item in data_guess["guesses"]:
                                if "score" in item:
                                    total_score_current_guess += item["score"]
                        logging.info(
                            "Guess Successful : Score {}\n".format(
                                total_score_current_guess
                            )
                        )
                        logging.info("Result : {}".format(data_guess))

                        guess_key = "Round-" + str(data["roundId"])

                        if key not in _MY_GUESS_TRACKER:
                            _MY_GUESS_TRACKER[key] = []

                        _MY_GUESS_TRACKER[key].append(data_guess)

    return "Game Move Done!"

@app.route("/apply/logic", methods=["POST"])
def apply_logic():
    error, data = get_game_status()
    game_status = game_status_received(error, data)
    time.sleep(5)
    response = create_task(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        uri="/apply/logic"
            )
    return "Task Created Successfully"


@app.route("/")
def root():
    logging.info(os.environ.get("GOOGLE_CLOUD_PROJECT", ""))
    team = _TEAM
    if team is None or _TEAM.strip() == "":
        logging.error(_TEAM_NOT_PROVIDED)
        return _TEAM_NOT_PROVIDED
    
    create_task(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        uri="/apply/logic",
    )
    logging.info("----------------------------------------------------------")
    logging.info("Game Started")
    logging.info("----------------------------------------------------------")
    logging.info("I am playing as {}".format(_TEAM))
    return "Game successfully started."


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)))
