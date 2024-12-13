from typing import TypedDict, Self


class JsonApiResponse[TData](TypedDict):
    data: TData


class JsonApiResource[TAttrib](TypedDict):
    id: str
    type: str
    attributes: TAttrib
    included: list[Self]


class CustomerAccountAttributes(TypedDict):
    account_number: str


class CustomerAccount(JsonApiResource[CustomerAccountAttributes]):
    type = "customer_account"


class CustomerIcpConsumerAttributes(TypedDict):
    icp_number: str
    supply_node_ref: str
    physical_address: str


class CustomerIcpConsumer(JsonApiResource[CustomerIcpConsumerAttributes]):
    type = "customer_icp_consumer"


class RatingRatedPeriodAttributes(TypedDict):
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


class RatingRatedPeriod(JsonApiResource[RatingRatedPeriodAttributes]):
    type = "rating_rated_period"


# TODO: Attributes
class RatingComponent(JsonApiResource):
    type = "rating_component"
