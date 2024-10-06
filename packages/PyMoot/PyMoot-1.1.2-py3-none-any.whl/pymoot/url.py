from typing import Final


class Url:
    ACCOUNT: Final[str] = "https://api.komoot.de/v006/account/email/{email}/"
    LIST_TOURS: Final[str] = "https://api.komoot.de/v007/users/{user_identifier}/tours/"
    ONE_TOUR: Final[str] = "https://api.komoot.de/v007/tours/{tour_identifier}"
    HIGHLIGHT_URL: Final[str] = 'https://api.komoot.de/v007/highlights/{highlight_identifier}'
