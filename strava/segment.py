from utils.base import StravaBaseClass

SEGMENT_EFFORTS = "/segment_efforts/{id}"
SEGMENT = "/segments/{id}"


class Segment(StravaBaseClass):
    pass
    # def __init__(self):
    #     super().__init__()


def get_segment(self, segment_id):
    segment = self.get(SEGMENT.format(id=segment_id))
    print(segment)
    print(segment['athlete_segment_stats'])
    print(segment['local_legend'])
    print(segment.keys())
    print(segment['athlete_segment_stats'].keys())
