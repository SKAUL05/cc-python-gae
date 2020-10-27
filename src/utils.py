from google.cloud import tasks_v2
import requests
import datetime
import google.cloud.logging
import logging

client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

def to_dict(response_obj):
    response_json = {}
    try:
        response_json = response_obj.json()
    except Exception as e:
        logging.error(e)
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
        logging.error(e)
        return "Exception Occurred", None
    finally:
        error = None
        data = None
        if response is None:
            error = "No Response"
            return error, data
        error, data, status = to_dict(response)

        return error, data


def create_task(
    project,
    uri,
    task_name=None,
    location="us-central1",
    queue="default",
    payload=None,
    in_seconds=None,
):

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project, location, queue)
    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
            "relative_uri": uri,
        }
    }
    if payload is not None:
        converted_payload = payload.encode()
        task["app_engine_http_request"]["body"] = converted_payload

    if in_seconds is not None:
        timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)
        task["schedule_time"] = timestamp

    if task_name is not None:
        # Add the name to tasks.
        task["name"] = "projects/{}/locations/{}/queues/{}/tasks/{}".format(
            project, location, queue, task_name
        )

    response = client.create_task(parent=parent, task=task)

    logging.info("Created task {}".format(response.name))
    return response
