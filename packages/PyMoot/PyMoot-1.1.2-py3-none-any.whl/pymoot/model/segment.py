from typing import Optional


class Segment:

    def __init__(self, segment_type: str, start: int, end: int, reference: Optional[str] = None):
        """
        Segment object.

        :param segment_type: type of segment
        :param start: start of the segment
        :param end: end of the segment
        :param reference: reference of the segment (optional)
        """
        self.segment_type: str = segment_type
        self.start: int = start
        self.end: int = end
        self.reference: Optional[str] = reference