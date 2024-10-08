import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional, List, Final, Union, Self

import gpxpy
import requests
from dateutil import parser
from gpxpy.gpx import GPX

from pymoot.auth import Auth
from pymoot.model.coordinate import Coordinate
from pymoot.model.difficulty import Difficulty
from pymoot.model.highlight import Highlight
from pymoot.model.komoot_image import KomootImage
from pymoot.model.segment import Segment
from pymoot.model.segment_information import SegmentInformation
from pymoot.model.sport_type import SportTypes
from pymoot.model.surface import Surface
from pymoot.model.tour_information import TourInformation
from pymoot.model.tour_summary import TourSummary
from pymoot.model.way_type import WayType
from pymoot.model.waypoint import Waypoint
from pymoot.url import Url

"""
Tour model description exists here: https://static.komoot.de/doc/external-api/v007/docson/index.html#../schemas/users_tours.schema.json
"""


class TourTypes:
    """Possible types of tours."""

    PLANNED: Final[str] = "tour_planned"
    RECORDED: Final[str] = "tour_recorded"

    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all possible tour types.

        :return: list of supported tour types
        """
        return [
            getattr(cls, attr) for attr in dir(cls) if not attr.startswith('__') and not callable(getattr(cls, attr))
        ]


class TourSortOrders:
    """Possible tour sort directions."""

    ASCENDING: Final[str] = "asc"
    DESCENDING: Final[str] = "desc"

    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all possible tour sort orders.

        :return: list of supported tour sort orders
        """
        return [
            getattr(cls, attr) for attr in dir(cls) if not attr.startswith('__') and not callable(getattr(cls, attr))
        ]


class TourSortFields:
    """
    List of tour fields allowed for sort.
    """
    DATE: Final[str] = "date"
    DURATION: Final[str] = "duration"
    ELEVATION: Final[str] = "elevation"
    NAME: Final[str] = "name"
    PROXIMITY: Final[str] = "proximity"

    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all possible sort fields.
        :return: A list of all supported sort fields
        """
        return [
            getattr(cls, attr) for attr in dir(cls) if not attr.startswith('__') and not callable(getattr(cls, attr))
        ]


class Tour:
    """Tour model."""
    def __init__(self, tour: Dict[str, Any], authentication: Auth):
        """
        Tour model.

        Tour model is described like that:
        - id (int): id of the tour
        - type (tour_planned, tour_recorded): type of the tour
        - status (private, public, friends): privacy status of the tour
        - source (str): source of the tour
        - date (int): timestamp when the tour recording started (for recorded tours) or when the tour was created
                      (for planned tours). ISO 8601 with milliseconds required
        - changed_at (int): timestamp when the last update of the tour occurred. ISO 8601 with milliseconds required
        - name (str) : name of the tour
        - kcal_active: effort estimation in kilocalories (active portion)
        - kcal_resting: effort estimation in kilocalories (resting portion)
        - start_point (Coordinate: first coordinate of the tour (with lat, lng and alt)
        - distance (int): 3D length of the tour, in meters
        - duration (int): Total duration from tour start to finish, in seconds - includes pauses
        - elevation_up (int): total elevation gain in meters
        - elevaton_down (int): total elevation loss in meters
        - sport (str): tour sport type
        - vector_map_image: dynamically rendered map with tour line
        - vector_map_image_preview: dynamically rendered map with tour line, proportioned for thumbnails
        - time_in_motion (int): estimation of actual time in motion (for recorded tours only)
        - constitution (int): constitution value used during planning (for planned tours only)
        - query (str): the query string of the tour (for planned tours only)
        - path (waipoints[]): list of waypoints used for planning the tour (for planned tours only)
        - segments (segment[]): describe the kind of the segments. A segment is the way in between two waypoints
                                (two elements of the path). Consequently the amount of path elements is always one
                                larger than the amount segments
        - tour_information: tour information dict containing:
          * type (FERRY|BICYCLE_DISMOUNT|MOVABLE_BRIDGE|UNSUITABLE|RESTRICTED|OFF_GRID|HEAVY_TRAFFIC|PRIVATE_LAND) :
              indicates type of information. e.g. OFF_GRID that the tour contains an off-grid segment. Clients must
              ignore unknown types
          * segments (list of segments informations)
        - summary: tour summary:
          * surfaces: list of surfaces with amount
          * way_types: list of way types with amount
        - difficulty: difficulty of the tour:
          * grade (difficult|moderate|easy)
          * explanation_technical (str): technical difficulty
          * explanation_fitness (str): physical difficulty
        - master_share_url (str): the web URL to this tour's canonical master tour

        :param tour: the tour as dict
        """
        self.auth = authentication
        self.id: str = tour["id"]
        self.type: str = tour["type"]
        self.status: str = tour["status"]
        self.source: str = tour["source"]
        self.date: datetime = parser.parse(tour["date"])
        self.changed_at: datetime = parser.parse(tour["changed_at"])
        self.name: str = tour["name"]
        self.kcal_active: float = tour["kcal_active"]
        self.kcal_resting: float = tour["kcal_resting"]
        self.start_point: Coordinate = Coordinate(lat=tour["start_point"]["lat"], lng=tour["start_point"]["lng"],
                                      alt=tour["start_point"]["alt"], time=None)
        self.distance: float = tour["distance"]
        self.duration: float = tour["duration"]
        self.elevation_up: float = tour["elevation_up"]
        self.elevation_down: float = tour["elevation_down"]
        if tour["sport"] not in SportTypes.list_all():
            raise ValueError(f"Unexpected sport type: {tour['sport']}")
        self.sport: str = tour["sport"]
        if "vector_map_image" in tour:
            self.vector_map_image = KomootImage(
                url=tour["vector_map_image"]["src"],
                templated=tour["vector_map_image"]["templated"] if "templated" in tour["vector_map_image"] else None,
                client_hash=tour["vector_map_image"]["client_hash"] if "client_hash" in tour["vector_map_image"]
                else None,
                attribution=tour["vector_map_image"]["attribution"] if "attribution" in tour["vector_map_image"]
                else None,
                attribution_url=tour["vector_map_image"]["attribution_url"] if "attribution_url"
                                                                               in tour["vector_map_image"] else None,
                media_type=tour["vector_map_image"]["type"] if "type" in tour["vector_map_image"] else None
            )
        else:
            self.vector_map_image = None
            logging.warning("No vector map image found")
        self.time_in_motion: Optional[int] = tour["time_in_motion"] if "time_in_motion" in tour else None
        self.constitution: Optional[int] = tour["constitution"] if "constition" in tour else None
        self.query: Optional[str] = tour["query"] if "query" in tour else None
        self.path: Optional[List[Waypoint]] = self._build_waypoints_list(tour["path"]) if "path" in tour else None
        self.segments: Optional[List[Segment]] = self._build_segments_list(tour["segments"]) \
            if "segments" in tour else None
        self.tour_information = self._build_tour_information_list(tour["tour_information"]) \
            if "tour_information" in tour else None
        self.summary = self._build_summary(tour["summary"]) if "summary" in tour else None
        if "difficulty" in tour:
            difficulty = tour["difficulty"]
            self.difficulty = Difficulty(grade=difficulty["grade"],
                                         explanation_technical=tour["difficulty"]["explanation_technical"],
                                         explanation_fitness=tour["difficulty"]["explanation_fitness"])
        self.master_share_url: str = tour["master_share_url"] if "master_share_url" in tour else None
        self.links_dict = tour['_links'] if '_links' in tour else None
        self.coordinates_link = None
        if self.links_dict is not None and "coordinates" in self.links_dict:
            self.coordinates_link = self.links_dict["coordinates"]["href"]
        self.coordinates: List[Coordinate] = []
        self.gpx_track: Optional[GPX] = None

        

    @staticmethod
    def _build_waypoints_list(path: List[Dict[str, Any]]) -> List[Waypoint]:
        """
        Build the list of waypoints from a path.

        :param path: the source path
        :return: list of waypoints
        """
        waypoints = []
        for waypoint in path:
            waypoints.append(Waypoint(
                location=Coordinate(lat=waypoint["location"]["lat"], lng=waypoint["location"]["lng"]),
                index=waypoint["index"],
                end_index=waypoint["end_index"] if "end_index" in waypoint else None,
                reference=waypoint["reference"] if "reference" in waypoint else None
            ))
        return waypoints

    @staticmethod
    def _build_segments_list(segments: List[Dict[str, Any]]) -> List[Segment]:
        """
        Build the list of segments from tour segments.

        :param segments: tour segments as list of dicts
        :return: final list of segments objects
        """
        final_segments = []
        for segment in segments:
            final_segments.append(Segment(
                segment_type=segment["type"],
                start=segment["from"],
                end=segment["to"],
                reference=segment["reference"] if "reference" in segment else None
            ))
        return final_segments

    @staticmethod
    def _build_tour_information_list(tour_information: List[Dict[str, Any]]) -> List[TourInformation]:
        """
        Build a list of tour information objects from tour information list.
        :param tour_information: list of tour information from API
        :return: list of TourInformation objects
        """
        tour_information_list = []
        for ti in tour_information:
            tour_information_list.append(
                TourInformation(
                    ti_type=ti["type"],
                    segments=[SegmentInformation(from_index=segment["from"], to_index=segment["to"])
                              for segment in ti["segments"]]
                )
            )
        return tour_information_list

    @staticmethod
    def _build_summary(summary_dict: Dict[str, Any]) -> TourSummary:
        """
        Build tour summary.
        :param summary_dict: summary dict from API
        :return: TourSummary object
        """
        return TourSummary(
            surfaces=[
                Surface(surface_type=surface["type"], amount=surface["amount"]) for surface in summary_dict["surfaces"]
            ],
            way_types=[
                WayType(way_type=way_type["type"], amount=way_type["amount"]) for way_type in summary_dict["way_types"]
            ]
        )

    def retrieve_coordinates(self) -> Optional[List[Coordinate]]:
        """
        Retrieve coordinates of the tour.

        :param authentication: authentication object
        :return: Coordinates, if any
        """
        if self.coordinates_link is not None:
            response = requests.get(
                url=self.coordinates_link,
                auth=(self.auth.get_email(), self.auth.get_password())
            ).json()["items"]
        else:
            logging.warning("No coordinates link exists for this tour")
            return None

        self.coordinates = [
            Coordinate(
                lat=coordinate["lat"],
                lng=coordinate["lng"],
                alt=coordinate["alt"] if "alt" in coordinate else None,
                time=coordinate["time"] if "time" in coordinate else None
            ) for coordinate in response
        ]
        return self.coordinates

    @classmethod
    def retrieve_tour_by_id(cls, tour_id: str, authentication: Auth, as_gpx: bool) -> Union[Self, GPX]:
        url_append = ""
        if as_gpx:
            url_append = ".gpx"
        response = requests.get(
            url=Url.ONE_TOUR.format(tour_identifier=tour_id) + url_append,
            auth=(authentication.get_email(), authentication.get_password()),
            params={"Type": "application/hal+json"}
        )
        if response.status_code == 403:
            raise ConnectionError("Connection to komoot field: invalid authentication")
        if response.status_code == 404:
            raise ValueError(f"No tour exists with id {tour_id}")
        if as_gpx:
            return gpxpy.parse(response.content)
        else:
            return Tour(response.json(), authentication=authentication)

    def retrieve_gpx(self) -> GPX:
        """
        Retrieve gpx data of a tour.

        :param authentication: authentication object
        :return: GPX data, if any
        """
        self.gpx_track = self.retrieve_tour_by_id(tour_id=self.id, authentication=self.auth, as_gpx=True)
        return self.gpx_track

    def retrieve_tour_highlights(self):
        """Retrieve tour highlights."""
        highlights = []
        if self.path is not None:
            for path in self.path:
                if path.reference is not None and (match := re.match(r"hl(p|s):(\d+)", path.reference)):
                    highlight_id = match.group(2)
                    response = requests.get(
                        url=Url.HIGHLIGHT_URL.format(highlight_identifier=highlight_id),
                        auth=(self.auth.get_email(), self.auth.get_password()),
                        headers={"content-encoding": "gzip", "content-type": "application/hal+json"}
                    )
                    if response.status_code == 403:
                        raise ConnectionError(
                            'Connection to Komoot API failed. Please check your credentials.'
                        )
                    highlight_dict = response.json()
                    highlights.append(Highlight(highlight_dict))
        else:
            logging.info("No highlights exists for this tour")
        return highlights
