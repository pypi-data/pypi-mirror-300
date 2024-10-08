import gzip
import json
import logging
import re
from io import BytesIO

import requests
import dateutil.parser as parser

from typing import Optional, List, Dict, Any, Union

from gpxpy.gpx import GPX

from pymoot.auth import Auth
from pymoot.model.sport_type import SportTypes
from pymoot.model.tour import Tour, TourTypes, TourSortOrders, TourSortFields
from pymoot.url import Url

logger = logging.getLogger("Connector")


class Connector:

    def __init__(self, email: str, password: str):
        """
        Connector to Komoot API.

        :param email: komoot user email
        :param password: komoot user password
        """
        self.auth = Auth(email=email, password=password)
        response = requests.get(Url.ACCOUNT.format(email=email), auth=(email, password))
        if response.status_code == 403:
            raise ConnectionError("Connection to Komoot failed. Please check your credentials")
        rdata = response.json()
        self.auth.set_username(rdata["username"])
        self.auth.set_token(rdata["password"])
        logger.info(f"Logged in as {email}")

    def get_tours(self,
                  limit: Optional[int] = None,
                  page: Optional[int] = None,
                  user_identifier: Optional[str] = None,
                  tour_type: Optional[str] = None,
                  center: Optional[str] = None,
                  max_distance: Optional[int] = None,
                  sport_types: Optional[List[str]] = None,
                  start_date: Optional[str] = None,
                  end_date: Optional[str] = None,
                  tour_name: Optional[str] = None,
                  sort_field: Optional[str] = None,
                  sort_direction: Optional[str] = None) -> List[Tour]:
        """
        Get list of tours from Komoot.

        :param limit: if given, max number of tours to return, else all tours are returned
        :param page: if given, number of page to return (with size given by limit), else return the first page
        :param user_identifier: user identifier to filter tours, if not provided the one of the authenticated user is
        used
        :param tour_type: tour type to return, if not given return all tupes
        :param center: the center of the search area
        :param max_distance: the max distance to the center given above
        :param sport_types: list of sport types to return
        :param start_date: filter tours more recent than this date
        :param end_date: filter tours older than this date
        :param tour_name: tour name to filter by
        :param sort_field: field to sort (default: date)
        :param sort_direction: direction of sort (default: ascending)
        :return: list of Tour objects
        """
        if user_identifier is None:
            user_identifier = self.auth.get_username()
        if tour_type is not None and tour_type not in TourTypes.list_all():
            raise ValueError(f"Unexpected tour type: {tour_type}")
        if center is not None:
            if not re.match(
                pattern=r"^[-+]?\d{1,2}(\.\d+)?,\s*[-+]?\d{1,3}(\.\d+)?$",
                string=center,
            ):
                raise ValueError(
                    f"Unexpected center: {center}. "
                    "Please provide a valid center in the format 'lat, lng' (e.g. '52.520008, 13.404954')."
                )
        if max_distance is None and center is not None:
            raise ValueError("Max distance is required if center is provided")
        if max_distance is not None and center is None:
            raise ValueError("Center is required if max distance is provided")
        if sport_types is not None:
            if not isinstance(sport_types, list):
                raise TypeError("sport_types must be a list")
            for sport_type in sport_types:
                if not isinstance(sport_type, str):
                    raise TypeError("Each sport type must be a string")
                if sport_type not in SportTypes.list_all():
                    raise ValueError(f"Unexpected sport type: {sport_type}")
        if start_date is not None:
            start_date = parser.parse(start_date)
        if end_date is not None:
            end_date = parser.parse(end_date)
        if start_date is not None and end_date is not None and start_date > end_date:
            raise ValueError("Start date must be before end date")
        if sort_field is not None and sort_field not in TourSortFields.list_all():
            raise ValueError(f"Sort on field {sort_field} is not allowed")
        if sort_field == TourSortFields.PROXIMITY and center is None:
            raise ValueError("To sort by proximity, you must provide a center")
        if sort_direction is not None and sort_direction not in TourSortOrders.list_all():
            raise ValueError(f"Unexpected sort_order value: {sort_direction}")

        query = {}
        if limit is not None:
            query["limit"] = limit
        if page is not None:
            query["page"] = page
        if tour_type is not None:
            query["type"] = tour_type
        if center is not None:
            query["center"] = center
        if max_distance is not None:
            query["max_distance"] = max_distance
        if sport_types is not None:
            query["sport_types"] = sport_types
        if start_date is not None:
            query["start_date"] = start_date
        if end_date is not None:
            query["end_date"] = end_date
        if tour_name is not None:
            query["name"] = tour_name
        if sort_direction is not None:
            query["sort_direction"] = sort_direction
        if sort_field is not None:
            query["sort_field"] = sort_field

        has_more = True
        current_page = 0
        tours = []
        while has_more:
            query["page"] = current_page
            response = self._get_page_of_tours(query=query, user_identifier=user_identifier)
            data = response.json()
            tour_list = data["_embedded"]
            tours.extend(tour_list["tours"])
            max_page = data["page"]["totalPages"]
            current_page = data["page"]["number"] + 1
            has_more = (current_page < max_page) if limit is None else False
        return [Tour(tour_dict, authentication=self.auth) for tour_dict in tours]

    def get_tour(self, tour_id: str, as_gpx=False) -> Union[Tour, GPX]:
        """
        Get a tour.

        :param tour_id: tour identifier
        :param as_gpx: if True, get GPX instead of the tour object
        :return:
        """
        return Tour.retrieve_tour_by_id(authentication=self.auth, tour_id=tour_id, as_gpx=as_gpx)

    def update_tour_title(
            self,
            tour_identifier: str,
            new_title: str
    ):
        """
        Get a tour by its ID.
        :param tour_identifier: The ID of the tour
        :param new_title: The new title of the tour
        """

        try:
            response = requests.patch(
                url=Url.ONE_TOUR.format(tour_identifier=tour_identifier),
                auth=(self.auth.get_email(), self.auth.get_password()),
                headers={"content-encoding": "gzip", "content-type": "application/hal+json"},
                data=self._zip_payload(json.dumps({"name": new_title}))
            )
            if response.status_code == 403:
                raise ConnectionError(
                    'Connection to Komoot API failed. Please check your credentials.'
                )
            if response.status_code == 404:
                raise ValueError(f'Invalid tour identifier provided: {tour_identifier}. '
                                 f'Please provide a valid tour identifier.')
            if response.status_code == 500:
                raise ConnectionError(
                    'Internal Server Error. if you requested a FIT file, '
                    'please try again later or try fetching another format.'
                )
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                'Connection to Komoot API failed. Please check your internet connection.'
            )
        resp = json.loads(response.content.decode('utf-8'))
        return Tour(resp, self.auth)

    def _get_page_of_tours(self, query: Dict[str, Any], user_identifier: str) -> requests.Response:
        """
        Get a page of tours.

        :param query: query arguments to add to the request
        :param user_identifier: the user identifier
        :return:
        """
        response = requests.get(
            url=Url.LIST_TOURS.format(user_identifier=user_identifier),
            auth=(self.auth.get_email(), self.auth.get_password()),
            params=query
        )
        if response.status_code == 403:
            raise ConnectionError("Connection to komoot field: invalid authentication")
        return response

    @staticmethod
    def _zip_payload(payload: str) -> bytes:
        btsio = BytesIO()
        g = gzip.GzipFile(fileobj=btsio, mode='w')
        g.write(bytes(payload, 'utf8'))
        g.close()
        return btsio.getvalue()
