from datetime import timedelta
from utils.base import StravaBaseClass
from utils.conversions import convert_speed, convert_distance, convert_elevation


ACTIVITY_LAPS = "/activities/{id}/laps"
ACTIVITY = "/activities/{id}"
ACTIVITY_STREAMS = "/activities/{id}/streams?keys=altitude,latlng&key_by_type=true"

SEGMENT_EFFORTS = "/segment_efforts"
SEGMENT = "/segments/{id}"


# Stolen from here: https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/convert.py#L290
def decode_polyline(polyline):
    """Decodes a Polyline string into a list of lat/lng dicts.

    See the developer docs for a detailed description of this encoding:
    https://developers.google.com/maps/documentation/utilities/polylinealgorithm

    :param polyline: An encoded polyline
    :type polyline: string

    :rtype: list of dicts with lat/lng keys
    """
    points = []
    index = lat = lng = 0

    while index < len(polyline):
        result = 1
        shift = 0
        while True:
            b = ord(polyline[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1f:
                break
        lat += (~result >> 1) if (result & 1) != 0 else (result >> 1)

        result = 1
        shift = 0
        while True:
            b = ord(polyline[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1f:
                break
        lng += ~(result >> 1) if (result & 1) != 0 else (result >> 1)

        points.append({"lat": lat * 1e-5, "lng": lng * 1e-5})

    return points


class Activity(StravaBaseClass):

    def __init__(self, activity_id):
        super().__init__()
        self.id = activity_id
        # self.laps = dict()
        # self.full_activity = dict()
        # self.laps = list()
        # self.get_activity()
        self.full_activity = self.get(ACTIVITY.format(id=self.id), True)
        self.laps = self.full_activity['laps']
        self.name = self.full_activity['name']
        self.distance = self.full_activity['distance']
        self.moving_time = self.full_activity['moving_time']
        self.total_elevation_gain = self.full_activity['total_elevation_gain']
        self.type = self.full_activity['type']
        self.sport_type = self.full_activity['sport_type']  # Probably get rid of this??
        self.start_date_local = self.full_activity['start_date_local']
        self.average_speed = self.full_activity['average_speed']
        self.average_heartrate = self.full_activity['average_heartrate']
        self.description = self.full_activity['description']
        self.similar_activities = self.full_activity['similar_activities']
        self.available_zones = self.full_activity['available_zones']  # No idea what this is yet

    def get_laps(self):
        self.laps = self.get(ACTIVITY_LAPS.format(id=self.id))
        print(self.laps[0])
        for lap in self.laps:
            print(f"{convert_distance(lap['distance'])} miles, {convert_elevation(lap['total_elevation_gain'])} feet")

    # def get_activity(self):
    #     self.full_activity = self.get(ACTIVITY.format(id=self.id), cache=True)
    #     self.laps = self.full_activity['laps']

    def print_activity(self):
        print(self.full_activity.keys())
        print(self.laps[3])
        print(self.full_activity['name'])
        for lap in self.laps:
            print(f"{convert_distance(lap['distance'])} miles, "
                  f"{lap['moving_time']}s, "
                  f"{convert_elevation(lap['total_elevation_gain'])} feet")
        print(self.full_activity['map'])
        print(self.full_activity['map']['polyline'])
        print(self.full_activity['map']['summary_polyline'])
        print(decode_polyline(self.full_activity['map']['polyline']))
        print(f"Number of datapoints in polyline: {len(decode_polyline(self.full_activity['map']['polyline']))}")
        print(decode_polyline(self.full_activity['map']['summary_polyline']))
        print(self.full_activity['external_id'])
        print(self.full_activity['segment_efforts'][0].keys())
        for segment in self.full_activity['segment_efforts']:
            # if segment['achievements']:
            #     print(segment)
            #     print(f"{segment['name']}: {segment['achievements']}")
            print(segment)
            print(f"{segment['name']}: {segment['segment']['id']}")
        # print(self.full_activity['segment_efforts'])
        print(self.full_activity['device_name'])

    # Requires strava subscription
    def get_segment_efforts(self, segment_id):
        print(self.get(SEGMENT_EFFORTS + f"?segment_id={segment_id}"))

    def get_segment(self, segment_id):
        segment = self.get(SEGMENT.format(id=segment_id))
        print(segment)
        print(segment['athlete_segment_stats'])
        print(segment['local_legend'])
        print(segment.keys())
        print(segment['athlete_segment_stats'].keys())

    def get_activity_streams(self):
        return self.get(ACTIVITY_STREAMS.format(id=self.id), cache=True)
        # streams = self.get(ACTIVITY_STREAMS.format(id=self.id), cache=True)
        # return streams['latlng']['data']

        # # print(streams['altitude']['data'])
        # # print(len(streams['altitude']['data']))
        # # print(streams['latlng']['data'])
        # # print(len(streams['latlng']['data']))
        # # print(streams)
        # # print(streams.keys())
        # if len(streams['altitude']['data']) != len(streams['latlng']['data']):
        #     print("streams are different length!!!")
        # # stream_count = min(len(streams['altitude']['data']), len(streams['latlng']['data']))-1
        # # stream_count = 5
        # # points = []
        # # points3d = []
        # # for i in range(stream_count):
        # #     points.append(Point(streams['latlng']['data'][i]))
        # #     points3d.append(Point(streams['latlng']['data'][i] + [streams['altitude']['data'][i]]))
        # #
        # #
        # # line = LineString(points)
        # # print(line)
        # # for altitude in streams['altitude']['data']:
        # #     streams['latlng']['data'].append(altitude)
        # #
        # # print(streams['latlng']['data'])
        #
        # # https://pythongis.org/part2/chapter-06/nb/00-introduction-to-geographic-objects.html
        #
        # # mixed_streams = zip(*zip(*streams['latlng']['data'][:5]), streams['altitude']['data'][:5])
        # mixed_streams = [
        #     (*streams['latlng']['data'][i],
        #      streams['altitude']['data'][i]) for i in range(len(streams['latlng']['data']))
        # ]
        # # mixed_streams = [
        # #     (*streams['latlng']['data'][i],
        # #      streams['altitude']['data'][i]) for i in range(5)
        # # ]
        #
        # line = LineString(streams['latlng']['data'])
        # line3d = LineString(mixed_streams)
        # poly = Polygon(mixed_streams)
        #
        # # print(list(line3d.coords))
        # # print(line3d.length)
        # # print(poly)
        #
        # weight = (365 - (date.today() - date.fromisoformat(self.full_activity['start_date_local'][:10])).days)/40
        # print(weight)
        #
        # m = folium.Map(location=streams['latlng']['data'][0], zoom_start=13)
        #
        # folium.PolyLine(
        #     streams['latlng']['data'],
        #     weight=weight
        # ).add_to(m)
        #
        # m.save("test.html")
        #
        # # print(streams['latlng']['data'][:3])
        # # print(*streams['latlng']['data'][:3])
        # # for i in [*streams['latlng']['data'][:3]]:
        # #     print(i)
        # # print(*zip(*streams['latlng']['data'][:3]))
        # # print(list(zip(*streams['latlng']['data'][:3])))
        # # print(list(zip(*zip(*streams['latlng']['data'][:3]), streams['altitude']['data'][:3])))

    def get_summary(self):
        fields = {
            'id': self.full_activity['id'],
            'name': self.full_activity['name'],
            'distance': self.full_activity['distance'],
            'moving_time': self.full_activity['moving_time'],
            'total_elevation_gain': self.full_activity['total_elevation_gain'],
            'type': self.full_activity['type'],
            'sport_type': self.full_activity['sport_type'],
            'start_date_local': self.full_activity['start_date_local'],
            'average_speed': self.full_activity['average_speed'],
            'average_heartrate': self.full_activity['average_heartrate'],
            'description': self.full_activity['description'],
            'similar_activities': self.full_activity['similar_activities'],
            'available_zones': self.full_activity['available_zones']
        }
        print(self.full_activity.keys())
        print(self.laps[3])
        print(self.full_activity['name'])
        print(fields)
        for field in fields.keys():
            data = fields[field]
            if field == "distance":
                data = convert_distance(fields[field])
            elif field == "total_elevation_gain":
                data = convert_elevation(fields[field])
            elif field == "moving_time":
                data = timedelta(seconds=fields[field])
            elif field == "average_speed":
                data = timedelta(seconds=convert_speed(fields[field]))
            print(f"{field}: {data}")
        return fields

    def __str__(self):
        return f"id: {self.id}"


if __name__ == '__main__':
    # pass
    a = Activity(10597697833)
    # a.get_summary()
    # a.get_activity()
    a.print_activity()
    # a.get_segment_efforts(1039762) # Lake loop segment
    # a.get_segment(1039762)
    # a.get_activity_streams()
