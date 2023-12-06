from config import _TEAM, _PASSWORD, _BASE_API
from utils import make_request
from requests.auth import HTTPBasicAuth


auth = HTTPBasicAuth(_TEAM, _PASSWORD)

join = f"{_BASE_API}/api/join"
status = f"{_BASE_API}/api/gamestatus"
guess = f"{_BASE_API}/api/guess"


def join_game():
    return make_request("POST", join, auth=auth)


def get_game_status():
    return make_request("GET", status)


def make_guess(request):
    headers = {"Content-Type": "application/json"}
    return make_request("POST", guess, auth=auth, headers=headers, data=request)
