from send_req import make_login_request
import json
import hashlib
import os.path
from getpass import getpass
import time

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
AUTHTOKEN_FILE = FILE_PATH + "/" + ".authtoken"
CREDS_FILE = FILE_PATH + "/" + ".creds"

def compute_md5_hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


def get_login_creds():
    data = None
    if not os.path.isfile(CREDS_FILE):
        with open(CREDS_FILE, "w") as f:
            data = {
                "u": input("Nirvana E-Mail: "),
                "p": compute_md5_hash(getpass())
            }
            json.dump(data, f)
    else:
        with open(CREDS_FILE, "r") as f:
            data = json.load(f)
    return data


def get_auth_token(creds):
    if os.path.isfile(AUTHTOKEN_FILE):
        with open(AUTHTOKEN_FILE, "r") as f:
            data = json.load(f)
            token = data["token"]
            expiry = data["expiry"]
            now = int(time.time())
            if now < int(expiry):
                return token

    with open(AUTHTOKEN_FILE, "w+") as f:
        response = make_login_request(creds["u"], creds["p"])
        if response:
            auth = response["results"][0]["auth"]
            token = auth["token"]
            data = {
                "expiry": auth["expires"],
                "token": token
            }
            json.dump(data, f)
            return token
    return None
