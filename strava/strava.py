import logging
import os

from datetime import datetime

import athlete
import map
import activity
import segment

run = []
run.append('athlete')
# run.append('map')
# run.append('activity')
# run.append('segment')

DEFAULT_LOG_LEVEL = logging.INFO

LOG_LEVEL = getattr(logging, os.environ["LOG_LEVEL"].upper()) \
        if "LOG_LEVEL" in os.environ.keys() else \
        DEFAULT_LOG_LEVEL

logging.basicConfig(format='[%(levelname)s]  %(asctime)s:  %(message)s', level=LOG_LEVEL)

if 'map' in run:
    # map.map_months(range(1, 13), year=2019, activity_filter=["Run"])
    map.map_months(range(1, datetime.now().month+1), year=2025, activity_filter=["Run"])

if 'activity' in run:
    # a = activity.Activity(ACTIVITY_ID)
    # a.get_summary()
    # a.get_activity()
    # a.print_activity()
    # a.get_activity_streams()
    pass

if 'segment' in run:
    s = segment.Segment()
    s.get_segment(1039762)
    # a.get_segment_efforts(1039762) # Lake loop segment
    # a.get_segment(1039762)
    pass

if 'athlete' in run:
    # conn = auth.Auth()
    # conn.update_refresh_token()
    a = athlete.Athlete()
    logging.info(a)
    athlete.print_stats(a)

if __name__ == '__main__':
    pass

