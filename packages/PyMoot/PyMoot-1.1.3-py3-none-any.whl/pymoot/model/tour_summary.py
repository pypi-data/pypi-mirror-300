from typing import List

from pymoot.model.surface import Surface
from pymoot.model.way_type import WayType


class TourSummary:

    def __init__(self, surfaces: List[Surface], way_types: List[WayType]):
        """
        Tour summary object.

        :param surfaces: list of surfaces
        :param way_types: list of way types
        """
        self.surfaces: List[Surface] = surfaces
        self.way_types: List[WayType] = way_types
