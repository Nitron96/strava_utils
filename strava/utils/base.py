import logging

from . import auth


ATHLETE_API = "/athlete"

auth_objects = auth.ManageAuth()


class StravaBaseClass:
    def __init__(self, athlete_id=0):

        # IF AUTH BROKEN TRY THIS!!!
        # self.auth.update_access_token()

        self.a = auth_objects.get_auth(athlete_id)
        if athlete_id:
            self.get = self.a.get

    # This only exists to try to determine athlete ID after auth object is created
    def get(self, api, cache=False, _first_attempt=True):
        auth_objects.log_auths()
        r = self.a.get(api, cache, _first_attempt)
        try:
            if "id" in r.keys() and api == ATHLETE_API:
                logging.info(f"Assumed athlete ID: {r['id']} based on ATHLETE_API and r.id")
                auth_objects.register_auth(r['id'], self.a)
                self.get = self.a.get
            elif "athlete" in r.keys() and "id" in r["athlete"].keys():
                logging.info(f"Assumed athlete ID: {r['athlete']['id']} based on r.athlete.id")
                auth_objects.register_auth(r['athlete']['id'], self.a)
                self.get = self.a.get
        except AttributeError:
            logging.debug(f"Received object type '{type(r)}' from auth.get")
        except KeyError:
            logging.debug(f"Unable to determine athleteID from keys")
        return r
