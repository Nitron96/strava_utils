import logging

from utils.base import StravaBaseClass

SEGMENT_EFFORTS = "/segment_efforts/{id}"
SEGMENT = "/segments/{id}"
STARRED_SEGMENTS = "/segments/starred"


class Segment(StravaBaseClass):
    # def __init__(self):
    #     super().__init__()

    def get_segment(self, segment_id):
        segment = self.get(SEGMENT.format(id=segment_id))
        logging.info(segment)
        logging.info(segment['athlete_segment_stats'])
        logging.info(segment['local_legend'])
        logging.info(segment.keys())
        logging.info(segment['athlete_segment_stats'].keys())

    def get_starred_segments(self):
        for segment in self.get(STARRED_SEGMENTS):
            logging.info(f"{segment['name']}: {segment['id']}")
            if "athlete_pr_effort" in segment:
                logging.info(f"(PR id: {segment['athlete_pr_effort']['id']}, PR activity_id: "
                             f"{segment['athlete_pr_effort']['activity_id']})")
