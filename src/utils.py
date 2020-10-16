import requests


def to_dict(response_obj):
    response_json = {}
    try:
        response_json = response_obj.json()
    except Exception as e:
        print(e)
        return "Exception Occurred", None, None
    finally:
        error = None
        data = None
        status_code = response_obj.status_code
        if "err" in response_json and response_json["err"] is not None:
            error = response_json["err"]
        if "data" in response_json and response_json["data"] is not None:
            data = response_json["data"]
        if error is None and data is None:
            return "Get Game Status Failed", None, None
        return error, data, status_code


def make_request(method, url, **kwargs):
    response = None
    try:
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
    except requests.exceptions.RequestException as e:
        print(e)
        return "Exception Occurred", None
    finally:
        error = None
        data = None
        if response is None:
            error = "No Response"
            return error, data
        error, data, status = to_dict(response)

        return error, data
