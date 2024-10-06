from typing import Dict, Any

from pymoot.model.coordinate import Coordinate

"""
Highlight model description exists here: https://static.komoot.de/doc/external-api/v007/docson/index.html#../schemas/highlight.schema.json
"""


class HighlightTypes:
    HIGHLIGHT_POINT = "highlight_point"
    HIGHLIGHT_SEGMENT = "highlight_segment"


class Highlight:
    def __init__(
            self,
            highlight: Dict[str, Any],
    ):
        """Representation of a highlight."""
        self.id = highlight["id"]
        self.type = highlight["type"]
        self.base_name = highlight["base_name"]
        self.name = highlight["name"]
        self.created_at = highlight["created_at"]
        self.changed_at = highlight["changed_at"]
        self.sport = highlight["sport"]
        self.start_point = Coordinate(
            lat=highlight["start_point"]["lat"],
            lng=highlight["start_point"]["lng"],
            alt=highlight["start_point"]["alt"]
        )
        self.mid_point = Coordinate(
            lat=highlight["mid_point"]["lat"],
            lng=highlight["mid_point"]["lng"],
            alt=highlight["mid_point"]["alt"]
        )
        self.end_point = Coordinate(
            lat=highlight["end_point"]["lat"],
            lng=highlight["end_point"]["lng"],
            alt=highlight["end_point"]["alt"]
        )
        self.distance = highlight["distance"]
        self.elevation_up = highlight["elevation_up"]
        self.elevation_down = highlight["elevation_down"]
        self.score = highlight["score"]
        self.poor_quality = highlight["poor_quality"]
        self.categories = highlight["categories"]
        self.flagged = highlight["flagged"],
        self.front_image = highlight["_embedded"]["front_image"]["src"].split("?")[0] \
            if ("_embedded" in highlight and "front_image" in highlight["_embedded"]
                and highlight["_embedded"]["front_image"] is not None) else None
