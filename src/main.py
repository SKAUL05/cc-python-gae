import os
import time
import json
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


def game_status_received(err, data):
    if err is not None:
        print(Fore.RED + err)
        print(Fore.RED + "Get Game Status Failed")
    else:
        print()
        print(
            Fore.YELLOW + "GameId:",
            data["gameId"],
            Fore.YELLOW + "RoundId:",
            data["roundId"],
            Fore.YELLOW + "State:",
            data["state"],
            Fore.YELLOW + "#Participants:",
            len(data["participants"]),
        )
        print(
            "------------------------------------------------------------------------------------------\n"
        )

        state = data["state"]
        key = str(data["gameId"]) + "-" + str(data["roundId"])
        joined_status = False
        alive_status = False
        team_name = _TEAM.upper()
        for participant in data["participants"]:
            if (
                "name" in participant
                and participant["name"] == team_name
                and participant["joinedInThisRound"] == True
            ):
                joined_status = True
                alive_status = participant["isAlive"]

        if state == "joining":

            if not joined_status:
                err_join, data_join = join_game()
                if err_join is not None:
                    print(Fore.RED + "Join Failed")
                    print(err_join)
                else:
                    print(Fore.GREEN + "Join Successful")
                    print(Fore.GREEN + data_join["message"])

            else:
                print(Fore.YELLOW + "Already joined, waiting to play...")

        elif state == "running":
            if not joined_status:
                print(
                    Fore.YELLOW
                    + "Oho, I have missed the joining phase, let me wait till the next round starts"
                )
            elif not alive_status:
                print(Fore.RED + "I am dead, waiting to respawn in next round...:(")
            else:
                my_next_guess = apply_guess(
                    data["gameId"],
                    data["roundId"],
                    data["secretLength"],
                    data["participants"],
                    _MY_GUESS_TRACKER,
                )
                if my_next_guess is not None and len(my_next_guess["guesses"]) > 0:
                    print("My guess: {}".format(my_next_guess), "\n")
                    json_object = json.dumps(my_next_guess)
                    err_guess, data_guess = make_guess(json_object)

                    if err_guess is not None:
                        print(Fore.RED + "Guess Failed\n")
                        print(err_guess, "\n")

                    else:
                        total_score_current_guess = 0
                        if (
                            "guesses" in data_guess
                            and data_guess["guesses"] is not None
                        ):
                            for item in data_guess["guesses"]:
                                if "score" in item:
                                    total_score_current_guess += item["score"]
                        print(
                            Fore.GREEN
                            + "Guess Successful : Score {}\n".format(
                                total_score_current_guess
                            )
                        )
                        print("Result : {}".format(data_guess))

                        guess_key = "Round-" + str(data["roundId"])

                        if key not in _MY_GUESS_TRACKER:
                            _MY_GUESS_TRACKER[key] = []

                        _MY_GUESS_TRACKER[key].append(data_guess)


@app.route("/apply/logic", methods=["POST"])
def apply_logic(request):
    error, data = get_game_status()
    game_status_received(error, data)
    time.sleep(5)
    return


@app.route("/")
def root():
    app_id = os.getenv('appId').split("~")[1]
    init(autoreset=True)
    team = _TEAM
    if team is None or _TEAM.strip() == "":
        print(Fore.RED + _TEAM_NOT_PROVIDED)
        return _TEAM_NOT_PROVIDED + app_id

    print()
    print("Game Started")
    print()
    print(Fore.GREEN + "I am playing as {}".format(_TEAM))
    return "Game successfully started."


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)))
