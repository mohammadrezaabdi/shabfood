from enum import IntEnum
from pydantic import BaseModel
from typing import Optional, List, Tuple


class Customer(BaseModel):
    id: str
    password: str
    address: str


class Deliverer_Status(IntEnum):
    IDLE = 0
    ON_DECISION = 1
    BUSY = 2


class Deliverer(BaseModel):
    id: str
    password: Optional[str]
    status: Deliverer_Status


class Food_Status(IntEnum):
    UNAVAILABLE = 0
    AVAILABLE = 1


class Food(BaseModel):
    id: Optional[str]
    name: str
    price: int
    status: Food_Status


class Restaurant(BaseModel):
    id: str
    name: str
    password: Optional[str]
    address: Optional[str]
    menu: Optional[List[Food]] = None


class Order_Status(IntEnum):
    RESTAURANT_PENDING = 0
    RESTAURANT_ACCEPT = 1
    DELIVERER_PENDING = 2
    DELIVERING = 3
    DONE = 4
    CANCEL = -1


class Order_item(BaseModel):
    food_id: str
    quantity: int


class Order(BaseModel):
    id: Optional[str]
    timestamp: str
    customer: Customer
    restaurant: Restaurant
    deliverer: Optional[Deliverer]
    items: Optional[List[Order_item]]
    status: Order_Status


def get_set_of_current_status_customer() -> list:
    return [Order_Status.RESTAURANT_PENDING,
            Order_Status.RESTAURANT_ACCEPT,
            Order_Status.DELIVERER_PENDING,
            Order_Status.DELIVERING]


def get_set_of_current_status_restaurant() -> list:
    return [Order_Status.RESTAURANT_PENDING,
            Order_Status.RESTAURANT_ACCEPT,
            Order_Status.DELIVERER_PENDING]


def get_set_of_current_status_deliverer() -> list:
    return [Order_Status.DELIVERING]


# The following functions are used to prevent any undefined transition (either intentionally or accidentally)
# between states of the order being done through update_order requests
def valid_order_status_transitions_restaurant() -> list:
    return [
        (Order_Status.RESTAURANT_PENDING, Order_Status.RESTAURANT_ACCEPT),
        (Order_Status.RESTAURANT_ACCEPT, Order_Status.DELIVERER_PENDING),
        (Order_Status.RESTAURANT_ACCEPT, Order_Status.DONE),

        (Order_Status.RESTAURANT_PENDING, Order_Status.CANCEL),
        (Order_Status.RESTAURANT_ACCEPT, Order_Status.CANCEL),
        (Order_Status.DELIVERER_PENDING, Order_Status.CANCEL)
    ]


def valid_order_status_transitions_deliverer() -> list:
    return [
        (Order_Status.DELIVERER_PENDING, Order_Status.DELIVERER_PENDING),
        (Order_Status.DELIVERER_PENDING, Order_Status.DELIVERING),
        (Order_Status.DELIVERING, Order_Status.DONE),

        (Order_Status.DELIVERING, Order_Status.CANCEL),
    ]
