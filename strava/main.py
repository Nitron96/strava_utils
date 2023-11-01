# https://developers.strava.com/docs/reference/#api-Athletes-getStats
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
STARRED_SEGMENTS = "/segments/starred"


METER_TO_MILE = 1609.344
METER_TO_KM = 1000

RUN_STATS = {"recent_run_totals", "all_run_totals", "ytd_run_totals"}
RUN_SUB_STATS = {"count", "distance", "moving_time", "elapsed_time", "elevation_gain"}


def to_rounded_miles(distance):
    return round(distance/METER_TO_MILE, 1)


def distance_str(distance):
    return f"{to_rounded_miles(distance)} mi ({distance/METER_TO_KM} km)"


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

    stats = dict[str, dict[str, int]]

    def __init__(self):
        self.auth = auth.Auth()
        self.auth.update_access_token()

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

        self.stats = self.get(STATS_API.format(id=self.id))

    def get(self, api):
        r = requests.get(BASE_URL + api, headers=self.auth.get_auth_bearer())
        return json.loads(r.text)

    def get_stats(self):
        print(f"All time distance:    {distance_str(self.stats['all_run_totals']['distance'])} miles")
        print(f"YTD time distance:    {distance_str(self.stats['ytd_run_totals']['distance'])} miles")
        print(f"Recent time distance: {distance_str(self.stats['recent_run_totals']['distance'])} miles")
        print(self.stats['ytd_run_totals'])
        print("----------------------------------------------\n")

    def daily_mileage_needed(self):
        days_remaining = (GOAL_DATE - date.today()).days
        miles_to_goal = GOAL_MILEAGE*METER_TO_MILE - self.stats['ytd_run_totals']['distance']
        print(f"Current mileage: {distance_str(self.stats['ytd_run_totals']['distance'])}")
        print(f"Remaining miles: {distance_str(miles_to_goal)}")
        print(f"Days remaining:  {days_remaining} ({round(days_remaining/7, 1)} weeks)")
        meters_per_day = miles_to_goal/days_remaining
        print(f"Miles per day:   {round(meters_per_day/METER_TO_MILE, 1)}")
        print(f"Miles per week:  {round(meters_per_day*7/METER_TO_MILE, 1)}")

    def get_starred_segments(self):
        for segment in self.get(STARRED_SEGMENTS):
            print(f"{segment['name']}: {segment['id']}")
            if "athlete_pr_effort" in segment:
                print(f"(PR id: {segment['athlete_pr_effort']['id']}, PR activity_id: "
                      f"{segment['athlete_pr_effort']['activity_id']})")

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.username}): {self.id}"


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(sys.version)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # conn = auth.Auth()
    # conn.update_refresh_token()
    athlete = Athlete()
    print(athlete)
    athlete.get_stats()
    athlete.daily_mileage_needed()
    # athlete.get_starred_segments()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
