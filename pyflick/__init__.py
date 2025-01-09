"""Python API For Flick Electric in New Zealand"""
from .authentication import AbstractFlickAuth
from .types import AuthException, CustomerAccount, RatingRatedPeriod, APIException, FlickPrice

import json_api_doc
import logging

_LOGGER = logging.getLogger(__name__)


class FlickAPI():
    """Python API For Flick Electric in New Zealand"""

    def __init__(self, auth: AbstractFlickAuth):
        self._auth: AbstractFlickAuth = auth

    async def __getJsonDoc(self, *args, **kwargs):
        response = await self._auth.request(*args, **kwargs)

        async with response:
            if (response.status in [401, 403]):
                _LOGGER.error("Auth error while fetching data")
                raise AuthException({
                    "status": response.status,
                    "message": await response.text()
                })
            if response.status != 200:
                _LOGGER.error("HTTP error while fetching data: [%s] %s", response.status, await response.text())
                raise APIException({
                    "status": response.status,
                    "message": await response.text()
                })

            api_response = await response.json()

            _LOGGER.debug("Raw response from API: %s", api_response)

            return json_api_doc.deserialize(api_response)

    async def getCustomerAccounts(self) -> list[CustomerAccount]:
        """Returns the accounts viewable by the current user."""
        _LOGGER.debug("Fetching customer accounts")

        return await self.__getJsonDoc("GET", "/customer/v1/accounts", params={
            "include": "main_consumer"
        })

    async def getPricing(self, supply_node: str) -> FlickPrice:
        """Gets current pricing for the given supply node."""
        _LOGGER.debug("Fetching pricing for %s", supply_node)

        period: RatingRatedPeriod = await self.__getJsonDoc("GET", "rating/v1/rated_period", params={
            "include": "components",
            "supply_node_ref": supply_node,
        })

        return FlickPrice(period)
