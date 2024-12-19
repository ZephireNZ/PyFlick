from abc import ABC, abstractmethod

from aiohttp import ClientSession, ClientResponse, FormData

from pyflick.types import AuthException

from .const import (
    DEFAULT_API_HOST,
    DEFAULT_AUTH_ENDPOINT,
    DEFAULT_CLIENT_ID,
    DEFAULT_CLIENT_SECRET
)

from urllib.parse import urljoin


class AbstractFlickAuth(ABC):
    """Abstract class to make authenticated requests.
    Allows for abstracted access token fetching/caching.
    """

    def __init__(self, websession: ClientSession,
                 host: str = DEFAULT_API_HOST):
        """Initialize the auth."""
        self.websession = websession
        self.host = host

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["Authorization"] = f"Bearer {access_token}"

        return await self.websession.request(
            method, urljoin(self.host, url), **kwargs, headers=headers,
        )


class SimpleFlickAuth(AbstractFlickAuth):
    """Simple implementation of AbstractFlickAuth that gets a token once using password grant."""
    def __init__(self, username: str, password: str,
                 websession: ClientSession,
                 client_id: str = DEFAULT_CLIENT_ID,
                 client_secret: str = DEFAULT_CLIENT_SECRET,
                 host: str = DEFAULT_API_HOST,
                 auth_url: str = DEFAULT_AUTH_ENDPOINT):
        super().__init__(websession, host)
        self._username = username
        self._password = password
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_url = auth_url

        self._token = None

    async def get_new_token(self, username: str, password: str,
                            client_id: str, client_secret: str
                            ) -> dict:
        """Generate access token object via the password grant."""
        data = FormData(fields={
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password
        })

        result = await self.websession.request(
            "POST", urljoin(self.host, self._auth_url), data=data
        )

        async with result:
            if result.status != 200:
                raise AuthException({
                    "status": result.status,
                    "message": await result.text()
                })

            return await result.json()

    async def async_get_access_token(self):
        if not self._token:
            ret = await self.get_new_token(self._username, self._password,
                                           self._client_id,
                                           self._client_secret)

            self._token = ret["id_token"]

        return self._token

