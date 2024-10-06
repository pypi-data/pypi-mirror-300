from typing import Optional

from pymoot.model.coordinate import Coordinate


class Waypoint:

    def __init__(self, location: Coordinate, index: int, end_index: Optional[int] = None,
                 reference: Optional[str] = None):
        """
        Waypoint object.

        :param location: latitude and longitude of waypoint
        :param index: an index (inclusive) into the tour coordinates array representing the location of the waypoint
        along the tour
        :param end_index: if the waypoint is a highlight segment, the segment ends at this index (exclusive) in the
        tour coordinate array
        :param reference: a namespaced reference to a highlight or OSM POI, e.g. "hl:85124"
        """
        self.location: Coordinate = location
        self.index: int = index
        self.end_index: Optional[int] = end_index
        self.reference: Optional[str] = reference
