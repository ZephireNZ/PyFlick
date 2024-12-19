from typing import TypedDict, Literal, Optional
from dateutil.parser import isoparse
from datetime import datetime as dt
from decimal import Decimal


class JsonApiResource(TypedDict):
    type: str
    id: str


class CustomerIcpConsumer(JsonApiResource):
    type = "customer_icp_consumer"
    icp_number: str
    supply_node_ref: str
    physical_address: str


class CustomerAccount(JsonApiResource):
    type = "customer_account"
    account_number: str
    address: str
    status: Literal["pending", "cancelled", "active", "closed"]
    main_consumer: Optional[CustomerIcpConsumer]


class RatingComponent(JsonApiResource):
    type = "rating_component"
    charge_method: str
    charge_setter: str
    value: str
    quantity: str
    unit_code: str
    charge_per: str
    flow_direction: str
    content_code: str
    hours_of_availability: int
    channel_number: int
    meter_serial_number: str
    price_name: str
    applicable_periods: list[str]
    single_unit_price: str
    billable: bool


class RatingRatedPeriod(JsonApiResource):
    type = "rating_rated_period"
    start_at: str
    end_at: str
    status: str
    cost: str
    import_cost: str
    export_cost: str
    cost_unit: str
    quantity: str
    import_quantity: str
    export_quantity: str
    quantity_unit: str
    renewable_quantity: str
    components: list[RatingComponent]


class APIException(Exception):
    pass


class AuthException(Exception):
    pass


class FlickPrice():
    def __init__(self, period: RatingRatedPeriod):
        self.raw: RatingRatedPeriod = period
        self.price: Decimal = Decimal(period["cost"])
        self.start_at: dt = isoparse(period["start_at"])
        self.end_at: dt = isoparse(period["end_at"])
        self.status: str = period["type"]
        self.components: list[PriceComponent] = [PriceComponent(c) for c in period["components"]]

    def __repr__(self):
        return f"FlickPrice({self.raw})"


class PriceComponent():
    def __init__(self, component: RatingComponent):
        # TODO: Fix attributes

        self.raw = component
        self.kind: str = component["charge_setter"]
        self.charge_method: str = component["charge_method"]
        self.charge_setter: str = component["charge_setter"]
        self.value: Decimal = Decimal(component["value"])
        self.quantity: Decimal = Decimal(component["quantity"])
        self.unit_code: str = component["unit_code"]
        self.charge_per: str = component["charge_per"]
        self.flow_direction: str = component["flow_direction"]

    def __repr__(self):
        return f"PriceComponent({self.raw})"
