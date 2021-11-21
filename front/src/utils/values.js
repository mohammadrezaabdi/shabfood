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

export const orderStateToColor = {
    "0": "warning",
    "1": "primary",
    "2": "secondary",
    "3": "primary",
    "4": "success",
    "-1": "error"
}