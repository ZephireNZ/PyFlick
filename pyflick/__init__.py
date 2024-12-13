"""Python API For Flick Electric in New Zealand"""
from .authentication import AbstractFlickAuth
from .const import DEFAULT_API_HOST
from .types import JsonApiResponse, CustomerAccount, CustomerIcpConsumer, RatingRatedPeriod, RatingComponent
from typing import List

from dateutil.parser import isoparse
from datetime import datetime as dt
from decimal import Decimal


class FlickPrice():
    def __init__(self, pricing: RatingRatedPeriod):
        attributes = pricing["attributes"]

        self.price: Decimal = Decimal(attributes["cost"])
        self.start_at: dt = isoparse(attributes["start_at"])
        self.end_at: dt = isoparse(attributes["end_at"])
        self.status: str = attributes["type"]
        self.components: List[PriceComponent] = [
            PriceComponent(c) for c in getComponents(pricing)]
        self.raw = pricing

    def __repr__(self):
        return f"FlickPrice({self.raw})"


class PriceComponent():
    def __init__(self, component: RatingComponent):
        # TODO: Fix attributes
        # attributes = component["attributes"]

        self.kind: str = component["kind"]
        self.charge_method: str = component["charge_method"]
        self.charge_setter: str = component["charge_setter"]
        self.value: Decimal = Decimal(component["value"])
        self.quantity: Decimal = Decimal(component["quantity"])
        self.unit_code: str = component["unit_code"]
        self.per: str = component["per"]
        self.flow_direction: str = component["flow_direction"]
        self.metadata: dict = component["metadata"]
        self.raw = component

    def __repr__(self):
        return f"PriceComponent({self.raw})"


class FlickAPI():
    """Python API For Flick Electric in New Zealand"""
    def __init__(self, auth: AbstractFlickAuth, host: str = DEFAULT_API_HOST):
        self._auth: AbstractFlickAuth = auth
        self._host: str = host

    async def getCustomerAccounts(self) -> list[CustomerAccount]:
        """Returns the accounts viewable by the current user."""

        response = await self._auth.request("GET", "/customer/v1/accounts", params={
            "include": "main_consumer"
        })

        async with response:
            if response.status != 200:
                raise APIException({
                    "status": response.status,
                    "message": await response.text()
                })

            api_response: JsonApiResponse[list[CustomerAccount]] = await response.json()

            return api_response["data"]

    async def getPricing(self, supply_node: str) -> FlickPrice:
        """Gets current pricing for the given supply node."""
        response = await self._auth.request("GET", "rating/v1/rated_periods", params={
            "include": "components",
            "supply_node_ref": supply_node,
        })

        async with response:
            if response.status != 200:
                raise APIException({
                    "status": response.status,
                    "message": await response.text()
                })

            api_response: JsonApiResponse[RatingRatedPeriod] = await response.json()

            return FlickPrice(api_response["data"])


class APIException(Exception):
    pass


def getSupplyNode(account: CustomerAccount) -> CustomerIcpConsumer:
    return next([x for x in account["included"] if x["type"] == CustomerIcpConsumer.type])


def getComponents(period: RatingRatedPeriod) -> list[RatingComponent]:
    return [x for x in period["included"] if x["type"] == RatingComponent.type]
