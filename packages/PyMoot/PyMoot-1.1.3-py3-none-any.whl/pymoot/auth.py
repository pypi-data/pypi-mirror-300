from typing import Optional


class Auth:
    def __init__(self, email: str, password: str):
        """
        Authentication object containing credentials.
        :param email: komoot user email
        :param password: komoot user password
        """
        if not email:
            raise ValueError("Username is required")
        if not password:
            raise ValueError("Password is required")
        self._email: str = email
        self._password: str = password
        self._token: Optional[str] = None
        self._username: Optional[str] = None

    def get_email(self) -> str:
        return self._email

    def get_password(self) -> str:
        return self._password

    def get_token(self) -> str:
        return self._token

    def get_username(self) -> str:
        return self._username

    def set_token(self, token: str) -> None:
        self._token = token

    def set_username(self, username: str) -> None:
        self._username = username

    def __str__(self):
        return f"""
        Authentication object:
        E-mail: {self._email}
        Password: {len(self._password) * "*"}
        Username: {self._username[:2]}...{self._username[-1:]}
        Token: {len(self._token) * "*" if self._token else None}
        """
