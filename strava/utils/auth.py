import json
import requests
import logging

from . import strava_cache as caching


REQUEST_LIMIT = 10  # Limit to 10 requests to strava api per run to avoid api limits

AUTHORIZE_URL = "https://www.strava.com/oauth/authorize?client_id={" \
                "}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&" \
                "scope=read,read_all,profile:read_all,activity:read,activity:read_all"

OATH_URL = "https://www.strava.com/oauth/token"
REFRESH_URL = "https://www.strava.com/api/v3/oauth/token"

BASE_URL = "https://www.strava.com/api/v3"


class RateLimitError(Exception):
    pass


class Auth:

    auths = []

    def __init__(self, athlete_id=0):
        self.auths.append(len(self.auths)+1)
        logging.info(f"Internal auth obj: {self.auths}")
        self.request_count = 0
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

    # Apparently needs to be done when permissions change
    def update_auth(self):
        r = requests.post(OATH_URL, data=self.get_auth_dict())
        response = json.loads(r.text)
        self.tokens["access_token"] = response["access_token"]
        self.tokens["refresh_token"] = response["refresh_token"]
        self.write_auth()

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

    def get(self, api, cache=False, _first_attempt=True):
        cache_identifier = api
        # If caching is enabled for this request, check if it exists and load it
        # print(caching.cache_hash(cache_identifier))
        if cache and caching.check(cache_identifier):
            return caching.load(cache_identifier)
        if self.request_count >= REQUEST_LIMIT:
            raise RateLimitError
        r = requests.get(BASE_URL + api, headers=self.get_auth_bearer())
        if r.status_code == 200:
            self.request_count += 1
            response = json.loads(r.text)
            # If caching is enabled for this request, save contents to cache
            if cache:
                caching.save(cache_identifier, response)
            return response
        elif _first_attempt and r.status_code == 401:
            print(f"Status code: {r.status_code}, attempting to refresh auth")
            self.update_access_token()
            return self.get(api, cache, _first_attempt=False)
        elif r.status_code == 429:
            self.request_count = REQUEST_LIMIT
            print(f"Status code: {r.status_code}, API limits hit")
        else:
            print(f"Status code: {r.status_code}")
        print(f"API call:    {api}")
        return json.loads(r.text)


# Needs to be run from here when authorizing new permissions for the app
if __name__ == '__main__':
    auth = Auth()
    auth.update_auth()
