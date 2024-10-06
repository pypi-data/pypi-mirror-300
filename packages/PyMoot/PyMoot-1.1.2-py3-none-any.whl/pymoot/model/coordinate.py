from typing import Optional


class Coordinate:
    def __init__(self, lat: float, lng: float, alt: Optional[float] = None, time: Optional[float] = None):
        """
        Coordinate object.

        :param lat: latitude
        :param lng: longitude
        :param alt: altitude in meters
        :param time: time, must be >=0 to precedent coordinate
        """
        # Check:
        self.check_lat(lat)
        self.check_lng(lng)
        self.check_alt(alt)
        self.check_time(time)

        # Assign:
        self.lat: float = lat
        self.lng: float = lng
        self.alt: Optional[float] = alt
        self.time: Optional[float] = time

    @staticmethod
    def check_lat(lat: float):
        if not -90 <= lat <= 90:
            raise ValueError(f"Invalid latitude: {lat}. Latitude must be between -90 and 90.")

    @staticmethod
    def check_lng(lng: float):
        if not -180 <= lng <= 180:
            raise ValueError(f"Invalid longitude: {lng}. Longitude mst be between -180 and 180.")

    @staticmethod
    def check_alt(alt: float):
        if alt is not None and not -1000 <= alt <= 10000:
            raise ValueError(
                f"Invalid altitude: {alt}. Altitude must be between -1000 and 10000.")

    @staticmethod
    def check_time(time: float):
        if time is not None and time < 0:
            raise ValueError(f"Invalid time: {time}. Time must be equal or above 0.")
