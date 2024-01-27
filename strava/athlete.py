# https://developers.strava.com/docs/reference/#api-Athletes-getStats
import json
import logging
from datetime import date, datetime

from utils.base import StravaBaseClass

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

GOAL_MILEAGE = 2000
GOAL_DATE = date(date.today().year, 12, 31)

BASE_URL = "https://www.strava.com/api/v3"
ATHLETE_API = "/athlete"
STATS_API = "/athletes/{id}/stats"

ACTIVITY_LIST = "/athlete/activities"
ACTIVITIES_PER_PAGE = 100


METER_TO_MILE = 1609.34
METER_TO_KM = 1000

RUN_STATS = {"recent_run_totals", "all_run_totals", "ytd_run_totals"}
RUN_SUB_STATS = {"count", "distance", "moving_time", "elapsed_time", "elevation_gain"}


def to_rounded_miles(distance):
    return round(distance/METER_TO_MILE, 1)


def distance_str(distance):
    return f"{to_rounded_miles(distance)} mi ({distance/METER_TO_KM} km)"


class Athlete(StravaBaseClass):

    # auth = auth.Auth()

    # id: int
    # username = str
    # firstname = str
    # lastname = str
    # city = str
    # state = str
    # country = str
    # sex = str
    # premium = bool

    # stats = dict[str, dict[str, int]]

    def __init__(self):
        super().__init__()

        athlete_data = self.get(ATHLETE_API, cache=True)

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

    def get_activities(self):
        activity_count = ACTIVITIES_PER_PAGE  # Start loop with "max" activities per page
        page_count = 0
        activities = []
        while activity_count == ACTIVITIES_PER_PAGE and page_count < 10:
            page_count += 1
            activity_page = self.get(ACTIVITY_LIST + f"?per_page={ACTIVITIES_PER_PAGE}&page={page_count}")
            activity_count = len(activity_page)  # Don't loop after there are less activities remaining
            activities.extend(activity_page)
            logging.info(f"found {len(activities)} activities so far, {len(activity_page)} this page")
        logging.info(f"Found a total of {len(activities)} activities.")
        # logging.info(f"Found a total of {len(activities)} activities, writing to json file.")
        # with open("../activities.json", 'w') as f:
        #     json.dump(activities, f)

    def get_activities_month(self, month, year, activity_filter=None):
        if activity_filter is None:
            activity_filter = []
        start = datetime(year, month, 1).timestamp()
        end = datetime(
            (year if month < 12 else year+1),   # If December set end year to next year
            (month+1 if month < 12 else 1),     # If December set end month to January
            1
        ).timestamp()
        activity_count = ACTIVITIES_PER_PAGE  # Start loop with "max" activities per page
        page_count = 0
        activities = []
        while activity_count == ACTIVITIES_PER_PAGE and page_count < 10:    # page limit in case api limits
            page_count += 1
            activity_page = self.get(
                ACTIVITY_LIST + f"?per_page={ACTIVITIES_PER_PAGE}&page={page_count}&"
                                f"before={end}&after={start}",
                # If year and month are different than today's date, we can cache the request
                cache=(year != date.today().year or month != date.today().month)
            )
            activity_count = len(activity_page)  # Don't loop after there are less activities remaining
            activities.extend(activity_page)
            logging.info(f"found {len(activities)} activities so far, {len(activity_page)} this page")
        logging.info(f"Found a total of {len(activities)} activities for {month}-{year}")
        # print(f"Found a total of {len(activities)} activities for {month}-{year}, writing to json file.")
        # with open(f"../activities_{month}_{year}.json", 'w') as f:
        #     json.dump(activities, f)
        # ids = []
        # for activity in activities:
        #     if not activity_filter or activity['type'] in activity_filter:
        #         ids.append(activity['id'])
        # print(ids)
        return activities

    def get_stats(self):
        logging.info(f"All time distance:    {distance_str(self.stats['all_run_totals']['distance'])}")
        logging.info(f"Year to Date:         {distance_str(self.stats['ytd_run_totals']['distance'])}")
        logging.info(f"Recent time distance: {distance_str(self.stats['recent_run_totals']['distance'])}")
        # print(self.stats['ytd_run_totals'])

    def daily_mileage_needed(self):
        days_remaining = (GOAL_DATE - date.today()).days
        miles_to_goal = GOAL_MILEAGE*METER_TO_MILE - self.stats['ytd_run_totals']['distance']
        logging.info(f"Current mileage: {distance_str(self.stats['ytd_run_totals']['distance'])}")
        logging.info(f"Remaining miles: {distance_str(miles_to_goal)}")
        logging.info(f"Days remaining:  {days_remaining} ({round(days_remaining/7, 1)} weeks)")
        meters_per_day = miles_to_goal/days_remaining
        logging.info(f"Miles per day:   {round(meters_per_day/METER_TO_MILE, 1)}")
        logging.info(f"Miles per week:  {round(meters_per_day*7/METER_TO_MILE, 1)}")

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.username}): {self.id}"


def print_stats(athlete):
    athlete.get_stats()
    athlete.daily_mileage_needed()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # conn = auth.Auth()
    # conn.update_refresh_token()
    athlete = Athlete()
    logging.info(athlete)
    print_stats(athlete)

    # athlete.get_activities()
    # athlete.get_activities_month(11, 2023, ["Run"])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
