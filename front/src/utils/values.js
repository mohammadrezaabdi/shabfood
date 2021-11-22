export const USER_TYPES = {
    customer: 'customer',
    deliverer: 'deliverer',
    restaurant: 'restaurant'
}

export const orderStateToStr = {
    "0": "RESTAURANT_PENDING",
    "1": "RESTAURANT_ACCEPT",
    "2": "DELIVERER_PENDING",
    "3": "DELIVERING",
    "4": "DONE",
    "-1": "CANCEL"
}

export const orderStatus = {
    RESTAURANT_PENDING: "0",
    RESTAURANT_ACCEPT: "1",
    DELIVERER_PENDING: "2",
    DELIVERING: "3",
    DONE: "4",
    CANCEL: "-1",
}


export const restaurantStateTransition = {
    "0": ["1", "-1"],
    "1": ["2", "4", "-1"],
    "2": ["-1"],
    "3": [],
    "4": [],
    "-1": []
}

export const delivererStatusTransition = {
    "2": ["3"],
    "3": ["4", "-1"],
}

export const orderStateToColor = {
    "0": "warning",
    "1": "primary",
    "2": "secondary",
    "3": "primary",
    "4": "success",
    "-1": "error"
}