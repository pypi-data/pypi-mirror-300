from typing import Final, List


class WayTypes:
    """
    List of available way types.

    Updated list is available here: https://static.komoot.de/doc/external-api/v007/waytypes.html
    """

    FERRY: Final[str] = "wt#ferry"
    ALPINE_BIKE_D9: Final[str] = "wt#alpine_bike_d9"
    ALPINE_BIKE_D8: Final[str] = "wt#alpine_bike_d8"
    TRAIL_D7: Final[str] = "wt#trail_d7"
    TRAIL_D6: Final[str] = "wt#trail_d6"
    TRAIL_D5: Final[str] = "wt#trail_d5"
    TRAIL_D4: Final[str] = "wt#trail_d4"
    TRAIL_D3: Final[str] = "wt#trail_d3"
    TRAIL_D2: Final[str] = "wt#trail_d2"
    TRAIL_D1: Final[str] = "wt#trail_d1"
    TRAIL: Final[str] = "wt#trail"
    HIKE_D9: Final[str] = "wt#hike_d9"
    HIKE_D8: Final[str] = "wt#hike_d8"
    HIKE_D7: Final[str] = "wt#hike_d7"
    HIKE_D6: Final[str] = "wt#hike_d6"
    HIKE_D5: Final[str] = "wt#hike_d5"
    HIKE_D4: Final[str] = "wt#hike_d4"
    HIKE_D3: Final[str] = "wt#hike_d3"
    HIKE_D2: Final[str] = "wt#hike_d2"
    HIKING_PATH: Final[str] = "wt#hiking_path"
    LONG_HIKING_PATH: Final[str] = "wt#long_hiking_path"
    ALPINE_HIKING_PATH: Final[str] = "wt#alpine_hiking_path"
    MOUNTAIN_HIKING_PATH: Final[str] = "wt#mountain_hiking_path"
    TRACK: Final[str] = "wt#track"
    WAY: Final[str] = "wt#way"
    MINOR_ROAD: Final[str] = "wt#minor_road"
    STREET: Final[str] = "wt#street"
    PRIMARY: Final[str] = "wt#primary"
    SERVICE: Final[str] = "wt#service"
    CYCLEWAY: Final[str] = "wt#cycleway"
    CYCLE_ROUTE: Final[str] = "wt#cycle_route"
    FOOTWAY: Final[str] = "wt#footway"
    MOVABLE_BRIDGE: Final[str] = "wt#movable_bridge"
    UNKNOWN: Final[str] = "wt#unknown"
    OFF_GRID: Final[str] = "wt#off_grid"

    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all possible way types.

        :return: list of supported way types
        """
        return [
            getattr(cls, attr) for attr in dir(cls) if not attr.startswith('__') and not callable(getattr(cls, attr))
        ]


class WayType:

    def __init__(self, way_type: str, amount: float):
        """
        Way type item object.

        :param way_type: type of way
        :param amount: percent (between 0 and 1) of this way type on the tour
        """
        if way_type not in WayTypes.list_all():
            raise ValueError(f"Unexpected way type: {way_type}")
        if not (0 <= amount <= 1):
            raise ValueError("Amount should be between 0 and 1")
        self.way_type: str = way_type
        self.amount: float = amount
