"""Python API For Flick Electric in New Zealand"""
from .authentication import AbstractFlickAuth
from .const import DEFAULT_API_HOST, DEFAULT_PRICE_ENDPOINT
from typing import List

from dateutil.parser import isoparse
from datetime import datetime as dt
from decimal import Decimal


class FlickAPI():
    """Python API For Flick Electric in New Zealand"""
    def __init__(self, auth: AbstractFlickAuth, host: str = DEFAULT_API_HOST):
        self._auth: AbstractFlickAuth = auth
        self._host: str = host

    async def getSupplyNode(self) -> str:
        response = await self._auth.request("GET", "/customer/v1/accounts?include=main_consumer", params={
            "include": "main_consumer"
        })

        async with response:
            if response.status != 200:
                raise APIException({
                    "status": response.status,
                    "message": await response.text()
                })

            return (await response.json())["data"]["main_consumer"]["supply_node_ref"]

    async def getPricing(self, supply_node: str, start_at: dt, end_at: dt) -> dict:
        response = await self._auth.request("GET", "rating/v1/rated_periods", params={
            "include": "components",
            "supply_node_ref": supply_node,
            "start_at": start_at.isoformat(),
            "end_at": end_at.isoformat(),
        })

        async with response:
            if response.status != 200:
                raise APIException({
                    "status": response.status,
                    "message": await response.text()
                })

            # TODO: Refactor
            return FlickPrice(await response.json())


class FlickPrice():
    def __init__(self, pricing: dict):
        needle = pricing["needle"]

        self.price: Decimal = Decimal(needle["price"])
        self.unit_code: str = needle["unit_code"]
        self.per: str = needle["unit_code"]
        self.start_at: dt = isoparse(needle["start_at"])
        self.end_at: dt = isoparse(needle["end_at"])
        self.now: dt = isoparse(needle["now"])
        self.type: str = needle["type"]
        self.components: List[PriceComponent] = [
            PriceComponent(c) for c in needle["components"]]
        self.raw = pricing

    def __repr__(self):
        return f"FlickPrice({self.raw})"


class PriceComponent():
    def __init__(self, component: dict):
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


class APIException(Exception):
    pass
