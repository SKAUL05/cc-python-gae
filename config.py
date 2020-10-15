import os

"""
For Running the app on your local machine, set the variables team and password as below
For example, if team is ALPHA and password is 12345
team = os.environ.get("TEAM", "ALPHA")
password = os.environ.get("PASSWORD", "12345")
"""
team = os.environ.get("TEAM", None)
password = os.environ.get("PASSWORD", None)
base_api = "localhost:5001"