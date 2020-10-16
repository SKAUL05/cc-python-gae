import os

"""
For Running the app on your local machine, set the variables team and password as below
For example, if team is ALPHA and password is 12345
team = os.environ.get("TEAM", "ALPHA")
password = os.environ.get("PASSWORD", "12345")
"""
_TEAM = os.environ.get("TEAM", None)
_PASSWORD = os.environ.get("PASSWORD", None)
_BASE_API = "localhost:5001"
