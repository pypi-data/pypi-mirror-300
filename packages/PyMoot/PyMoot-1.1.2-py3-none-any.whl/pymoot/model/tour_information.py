from typing import List

from pymoot.model.segment_information import SegmentInformation


class TourInformation:

    def __init__(self, ti_type: str, segments: List[SegmentInformation]):
        """
        Tour information object
        :param ti_type: type of tour information
        :param segments: list of segment information
        """
        self.ti_type: str = ti_type
        self.segments: List[SegmentInformation] = segments
