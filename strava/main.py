# This is a sample Python script.
import sys
import auth
import requests
import json
from datetime import date

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

GOAL_MILEAGE = 2000
GOAL_DATE = date(2023, 12, 31)

BASE_URL = "https://www.strava.com/api/v3"
ATHLETE_API = "/athlete"
STATS_API = "/athletes/{id}/stats"


METER_TO_MILE_CONVERSION = 1609.344

RUN_STATS = {"recent_run_totals", "all_run_totals", "ytd_run_totals"}
RUN_SUB_STATS = {"count", "distance", "moving_time", "elapsed_time", "elevation_gain"}


class Athlete:

    auth = auth.Auth

    id = int
    username = str
    firstname = str
    lastname = str
    city = str
    state = str
    country = str
    sex = str
    premium = bool

    def __init__(self):
        self.auth = auth.Auth()
        self.auth.update_refresh_token()

        # r = requests.get(BASE_URL + ATHLETE_API, headers=conn.get_auth_bearer())
        # athlete_data = json.loads(r.text)
        athlete_data = self.get(ATHLETE_API)

        self.id = athlete_data['id']
        self.username = athlete_data['username']
        self.firstname = athlete_data['firstname']
        self.lastname = athlete_data['lastname']
        self.city = athlete_data['city']
        self.state = athlete_data['state']
        self.country = athlete_data['country']
        self.sex = athlete_data['sex']
        self.premium = athlete_data['premium']

        self.stats = dict

    def get(self, api):
        r = requests.get(BASE_URL + api, headers=self.auth.get_auth_bearer())
        return json.loads(r.text)

    def get_stats(self):
        self.stats = self.get(STATS_API.format(id=self.id))
        print(f"All time distance:    {self.stats['all_run_totals']['distance']/METER_TO_MILE_CONVERSION} miles")
        print(f"YTD time distance:    {self.stats['ytd_run_totals']['distance']/METER_TO_MILE_CONVERSION} miles")
        print(f"Recent time distance: {self.stats['recent_run_totals']['distance']/METER_TO_MILE_CONVERSION} miles")

    def daily_mileage_needed(self):
        print(f"Current mileage: {self.stats['ytd_run_totals']['distance']/METER_TO_MILE_CONVERSION}")
        days_remaining = (GOAL_DATE - date.today()).days
        miles_to_goal = GOAL_MILEAGE*METER_TO_MILE_CONVERSION - self.stats['ytd_run_totals']['distance']
        print(f"Remaining miles: {miles_to_goal/METER_TO_MILE_CONVERSION}")
        print(f"Days remaining: {days_remaining}")
        print(f"Miles per day: {miles_to_goal/days_remaining/METER_TO_MILE_CONVERSION}")

    def __str__(self):
        return f"{self.username} ({self.firstname} {self.lastname}): {self.id}"


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(sys.version)


# def get_user_data(conn):
#     r = requests.get(BASE_URL+ATHLETE_API, headers=conn.get_auth_bearer())
#     user = Athlete(json.loads(r.text))
#     return user


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # conn = auth.Auth()
    # conn.update_refresh_token()
    athlete = Athlete()
    print(athlete)
    athlete.get_stats()
    athlete.daily_mileage_needed()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
