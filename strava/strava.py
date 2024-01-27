import logging
import os

import athlete
import map
import activity


# run = 'athlete'
run = 'map'
# run = 'activity'

DEFAULT_LOG_LEVEL = logging.INFO

LOG_LEVEL = getattr(logging, os.environ["LOG_LEVEL"].upper()) \
        if "LOG_LEVEL" in os.environ.keys() else \
        DEFAULT_LOG_LEVEL

logging.basicConfig(format='[%(levelname)s]  %(asctime)s:  %(message)s', level=LOG_LEVEL)

if run == 'athlete':
    # conn = auth.Auth()
    # conn.update_refresh_token()
    a = athlete.Athlete()
    logging.info(a)
    athlete.print_stats(a)

if run == 'map':
    # map_months(range(1, 13), year=2023, activity_filter=["Run"])
    map.map_months([1], year=2024, activity_filter=["Run"])

if run == 'activity':
    # a = activity.Activity(ACTIVITY_ID)
    # a.get_summary()
    # a.get_activity()
    # a.print_activity()
    # a.get_segment_efforts(1039762) # Lake loop segment
    # a.get_segment(1039762)
    # a.get_activity_streams()
    pass

if __name__ == '__main__':
    pass

