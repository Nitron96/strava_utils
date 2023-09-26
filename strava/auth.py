import json
import requests


AUTHORIZE_URL = "http://www.strava.com/oauth/authorize?client_id={" \
                "}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read "

OATH_URL = "https://www.strava.com/oauth/token"
REFRESH_URL = "https://www.strava.com/api/v3/oauth/token"


class Auth:

    tokens = {}

    def __init__(self):
        self.get_auth()
        with open("../auth.json") as f:
            self.tokens = json.load(f)

    def write_auth(self):
        with open("../auth.json", 'w') as f:
            json.dump(self.tokens, f)

    def get_auth(self):
        return self.tokens

    def get_auth_url(self):
        return AUTHORIZE_URL.format(self.tokens["client_id"])

    def get_auth_dict(self):
        return {
            "client_id": self.tokens["client_id"],
            "client_secret": self.tokens["client_secret"],
            "code": self.tokens["authorization_code"],
            "grant_type": "authorization_code"
        }

    def get_refresh_dict(self):
        return {
            "client_id": self.tokens["client_id"],
            "client_secret": self.tokens["client_secret"],
            "refresh_token": self.tokens["refresh_token"],
            "grant_type": "refresh_token"
        }

    def update_access_token(self):
        r = requests.post(REFRESH_URL, data=self.get_refresh_dict())
        response = json.loads(r.text)
        self.tokens["access_token"] = response["access_token"]
        self.tokens["refresh_token"] = response["refresh_token"]
        self.write_auth()

    def get_auth_bearer(self):
        return {"Authorization": f"Bearer {self.tokens['access_token']}"}
