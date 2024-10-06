class SegmentInformation:

    def __init__(self, from_index: int, to_index: int):
        """
        Segment information object.
        :param from_index: start index point (inclusive)
        :param to_index: stop index point (exclusive)
        """
        self.from_index: int = from_index
        self.to_index: int = to_index