import os
import unittest
from unittest.mock import patch, MagicMock

from pymoot.connector import Connector
from pymoot.model.tour import Tour
from tests.mock import mock_response


class TestConnector(unittest.TestCase):

    @classmethod
    @patch("requests.get")
    def setUpClass(cls, mock_get: MagicMock):
        cls.email = "test@example.com"
        cls.password = "password"
        cls.valid_id = "123456"
        cls.invalid_id = "invalid"
        mock_response(mock_req=mock_get,
                      status_code=200,
                      json_response=f"{os.path.dirname(os.path.realpath(__file__))}/resources"
                                    f"/authentication_response.json")
        cls.connector = Connector(email="test@example.com", password="password")

    @patch("requests.get")
    def test_initialization(self, mock_get: MagicMock):
        mock_response(
            mock_req=mock_get,
            status_code=200,
            json_response=f"{os.path.dirname(os.path.realpath(__file__))}/resources/authentication_response.json",
        )
        connector = Connector(
            email=self.email,
            password=self.password,
        )
        self.assertIsInstance(connector, Connector)

    @patch("requests.get")
    def test_get_tours(self, mock_get):
        mock_response(
            mock_req=mock_get,
            status_code=200,
            json_response=f"{os.path.dirname(os.path.realpath(__file__))}/resources/list_tours_response.json",
        )

        tours = self.connector.get_tours(limit=5)
        self.assertIsInstance(tours, list)
        for tour in tours:
            self.assertIsInstance(tour, Tour)
        self.assertEqual(5, len(tours))

    @patch("requests.get")
    def test_get_tour_by_valid_id(self, mock_get):
        mock_response(
            mock_req=mock_get,
            status_code=200,
            json_response=f"{os.path.dirname(os.path.realpath(__file__))}/resources/get_tour_by_id_response.json",
        )
        tour = self.connector.get_tour(tour_id=self.valid_id)
        self.assertIsInstance(tour, Tour)
