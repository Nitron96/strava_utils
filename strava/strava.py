import logging
import os

import athlete
import map
import activity

LOG_LEVEL = getattr(logging, os.environ["LOG_LEVEL"].upper()) if "LOG_LEVEL" in os.environ.keys() else logging.INFO

logging.basicConfig(level=LOG_LEVEL)

if __name__ == '__athlete__':
    # conn = auth.Auth()
    # conn.update_refresh_token()
    a = athlete.Athlete()
    print(a)
    athlete.print_stats(a)

if __name__ == '__map__':
    # map_months(range(1, 13), year=2023, activity_filter=["Run"])
    map.map_months([1], year=2024, activity_filter=["Run"])

if __name__ == '__activity__':
    # pass
    a = activity.Activity(ACTIVITY_ID)
    # a.get_summary()
    # a.get_activity()
    # a.print_activity()
    # a.get_segment_efforts(1039762) # Lake loop segment
    a.get_segment(1039762)
    # a.get_activity_streams()
