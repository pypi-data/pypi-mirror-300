from typing import List, Final


class SurfaceTypes:
    """
    List of available surfaces.

    Updated list can be found here: https://static.komoot.de/doc/external-api/v007/surfaces.html
    """

    # Bike:
    BIKE_ASPHALT: Final[str] = "sb#asphalt"
    BIKE_CONCRETE: Final[str] = "sb#concrete"
    BIKE_PAVED: Final[str] = "sb#paved"
    BIKE_PAVING_STONES: Final[str] = "sb#paving_stones"
    BIKE_COBBLESTONES: Final[str] = "sb#cobblestone"
    BIKE_COBBLES: Final[str] = "sb#cobbles"
    BIKE_COMPACTED_GRAVEL: Final[str] = "sb#compacted"
    BIKE_GRAVEL: Final[str] = "sb#gravel"
    BIKE_GRASS_PAVER: Final[str] = "sb#grass_paver"
    BIKE_WOOD: Final[str] = "sb#wood"
    BIKE_SAND: Final[str] = "sb#sand"
    BIKE_GROUND: Final[str] = "sb#ground"
    BIKE_STONE: Final[str] = "sb#stone"
    BIKE_UNPAVED: Final[str] = "sb#unpaved"
    BIKE_ALPINE: Final[str] = "sb#alpin"
    BIKE_UNKNOWN: Final[str] = "sb#unknown"

    # Foot:
    FOOT_ASPHALT: Final[str] = "sf#asphalt"
    FOOT_CONCRETE: Final[str] = "sf#concrete"
    FOOT_COBBLESTONES: Final[str] = "sf#cobblestone"
    FOOT_PAVING_STONES: Final[str] = "sf#paving_stones"
    FOOT_PAVED: Final[str] = "sf#paved"
    FOOT_COMPACTED_GRAVEL: Final[str] = "sf#compacted"
    FOOT_GRAVEL: Final[str] = "sf#gravel"
    FOOT_GRASS_PAVER: Final[str] = "sf#grass_paver"
    FOOT_WOOD: Final[str] = "sf#wood"
    FOOT_UNPAVED: Final[str] = "sf#unpaved"
    FOOT_SAND: Final[str] = "sf#sand"
    FOOT_GROUND: Final[str] = "sf#ground"
    FOOT_STONE: Final[str] = "sf#stone"
    FOOT_NATURAL: Final[str] = "sf#nature"
    FOOT_ALPINE: Final[str] = "sf#alpin"
    FOOT_UNKNOWN: Final[str] = "sf#unknown"

    # MTB:
    MTB_ASPHALT: Final[str] = "sm#asphalt"
    MTB_CONCRETE: Final[str] = "sm#concrete"
    MTB_COBBLESTONES: Final[str] = "sm#cobblestone"
    MTB_PAVING_STONES: Final[str] = "sm#paving_stones"
    MTB_PAVED: Final[str] = "sm#paved"
    MTB_COMPACTED_GRAVEL: Final[str] = "sm#compacted"
    MTB_GRAVEL: Final[str] = "sm#gravel"
    MTB_GRASS_PAVER: Final[str] = "sm#grass_paver"
    MTB_WOOD: Final[str] = "sm#wood"
    MTB_UNPAVED: Final[str] = "sm#unpaved"
    MTB_SAND: Final[str] = "sm#sand"
    MTB_GROUND: Final[str] = "sm#ground"
    MTB_STONE: Final[str] = "sm#stone"
    MTB_NATURAL: Final[str] = "sm#nature"
    MTB_ALPINE: Final[str] = "sm#alpin"
    MTB_UNKNOWN: Final[str] = "sm#unknown"

    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all possible surfaces.

        :return: list of supported surfaces
        """
        return [
            getattr(cls, attr) for attr in dir(cls) if not attr.startswith('__') and not callable(getattr(cls, attr))
        ]


class Surface:

    def __init__(self, surface_type: str, amount: float):
        """
        Surface item object.

        :param surface_type: type of the surface
        :param amount: percent (between 0 and 1) of this surface on the tour
        """
        if surface_type not in SurfaceTypes.list_all():
            raise ValueError(f"Unexpected surface type: {surface_type}")
        if not (0 <= amount <= 1):
            raise ValueError("Amount should be between 0 and 1")
        self.surface_type: str = surface_type
        self.amount: float = amount
