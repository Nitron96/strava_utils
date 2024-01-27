from datetime import date, timedelta

import folium
import logging

import activity
from athlete import Athlete
from utils.conversions import convert_speed, convert_distance, convert_elevation

STRAVA_ACTIVITY_URL = "https://www.strava.com/activities/{id}"


POPUP_HTML = """
<h3><a href="{url}" target=”_blank”>{name}</a></h3>
<h4>Distance: {distance}</h4>
<h4>Time: {time}</h4>
<h4>Pace: {pace}</h4>
<h4>Elevation: {elevation}</h4>
"""


def line_color(start_date):
    # hex_color = hex(int((365 - (date.today() - date.fromisoformat(start_date[:10])).days)/365*16777215))
    # logging.info(hex_color)
    # return f'#{str(hex_color)[2:]}'
    hex_color = hex(int((date.today() - date.fromisoformat(start_date[:10])).days/365*16777215))
    int_color = int((date.today() - date.fromisoformat(start_date[:10])).days/365*16777215)
    int_color_red = (255 << 16) - int_color
    int_color_tint = int_color + (255 << 4) + (255 << 12)
    # int_color_red = 255 - (int_color >> 16) & 255
    # logging.info(f"{int_color:#0{8}x}"[2:])
    # return f'#{str(hex_color)[2:]}'
    return '#'+f"{int_color_tint:#0{8}x}"[2:]


class Map:

    def __init__(self, center, zoom=13):
        self.m = folium.Map(location=center, zoom_start=zoom, tiles=None)
        # self.m = folium.Map(location=center, zoom_start=zoom)
        # self.m = folium.Map(location=center, zoom_start=zoom, tiles="cartodbpositron")

    def add_line(self, stream, color, tooltip, opacity=0.8, weight=8, popup=None):
        path = folium.PolyLine(
            stream,
            color=color,
            weight=weight,
            tooltip=tooltip,
            opacity=opacity
        ).add_to(self.m)
        if popup:
            path.add_child(folium.Popup(popup, max_width=250))

    def save(self, filename="test.html"):
        logging.info(f"Writing map to file: {filename}")
        self.m.save(filename)
        logging.info(f"Done writing file: {filename}")


def map_months(months, year=2023, activity_filter=None):
    if activity_filter is None:
        activity_filter = []
    logging.info("getting athlete")
    athlete = Athlete()
    logging.info("got athlete")
    activity_list = []
    for month in months:
        for act in athlete.get_activities_month(month, year):
            if not activity_filter or act['type'] in activity_filter:
                activity_list.append(act['id'])
    activities = []
    for a_id in activity_list:
        activities.append(activity.Activity(a_id))
    map_obj = Map(activities[0].full_activity['start_latlng'])
    for a in activities:
        # map_obj.add_line(
        #     a.get_activity_streams(),
        #     line_color(a.full_activity['start_date_local']),
        #     a.full_activity['name']
        # )
        streams = a.get_activity_streams()
        popup_contents = POPUP_HTML.format(
            url=STRAVA_ACTIVITY_URL.format(id=a.id),
            name=a.name,
            distance=convert_distance(a.distance),
            time=timedelta(seconds=a.moving_time),
            pace=timedelta(seconds=convert_speed(a.average_speed)),
            elevation=convert_elevation(a.total_elevation_gain)
        )
        if 'latlng' in streams.keys():
            logging.info(f"  Adding {a.full_activity['name']} to map")
            map_obj.add_line(
                streams['latlng']['data'],
                "#af5800",
                # "#B95200",
                a.full_activity['name'],
                opacity=0.2,
                weight=2,
                popup=popup_contents
            )
        else:
            logging.info(f"Skipping {a.full_activity['name']} as no 'latlng'")

    map_obj.save(f"{year}.html")


if __name__ == '__main__':
    # map_months(range(1, 13), year=2023, activity_filter=["Run"])
    map_months([1], year=2024, activity_filter=["Run"])
    # activities = []
    # for a_id in ACTIVITY_IDS:
    #     activities.append(activity.Activity(a_id))
    # map_obj = Map(activities[0].full_activity['start_latlng'])
    # for a in activities:
    #     logging.info(f"adding {a.full_activity['name']}")
    #     # map_obj.add_line(
    #     #     a.get_activity_streams(),
    #     #     line_color(a.full_activity['start_date_local']),
    #     #     a.full_activity['name']
    #     # )
    #     map_obj.add_line(
    #         a.get_activity_streams(),
    #         "#af5800",
    #         # "#B95200",
    #         a.full_activity['name'],
    #         opacity=0.1,
    #         weight=4
    #     )
    #
    # map_obj.save()
