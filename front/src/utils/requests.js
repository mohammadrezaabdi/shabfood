import axios from 'axios'

const server_addr = "http://shabfood.ir:80/api"

export const getRestaurant = (restID) => {
    return axios
        .get(`${server_addr}/restaurant/${restID}`)
}

export const getAllRestaurant = () => {
    return axios
        .get(`${server_addr}/restaurant/all`)
}

export function loginSubmit(formValues) {
    let params = { password: formValues.password }
    params[formValues.userType + "_id"] = formValues.userID
    return axios
        .post(`${server_addr}/${formValues.userType}/signin`,
            null, { params: params })
}

export function registerSubmit(formValues) {
    return axios
        .put(`${server_addr}/customer/signup`,
            {
                password: formValues.password,
                id: formValues.userID,
                address: formValues.address
            })
}

export function orderSubmit(restID, foodList, access_token) {
    return axios
        .put(`${server_addr}/customer/order/create`,
            foodList
            , {
                params: { restaurant_id: restID },
                headers: { Authorization: `Bearer ${access_token}` }
            })
}

export function getCustomerOrders(access_token) {
    return axios
        .get(`${server_addr}/customer/order/currents`,
            {
                headers: { Authorization: `Bearer ${access_token}` }
            })

}

export function getRestaurantOrder(access_token) {
    return axios
        .get(`${server_addr}/restaurant/order/currents`,
            {
                headers: { Authorization: `Bearer ${access_token}` }
            })

}

export function getDelivererCurrent(access_token) {
    return axios
        .get(`${server_addr}/deliverer/order/current`,
            {
                headers: { Authorization: `Bearer ${access_token}` }
            })
}

export function getDelivererRequest(access_token) {
    return axios
        .get(`${server_addr}/deliverer/order/request`,
            {
                headers: { Authorization: `Bearer ${access_token}` }
            })

}

export function updateOrderRestaurant(access_token, new_status, orderID) {
    return axios
        .post(`${server_addr}/restaurant/order/update`,
            null, {
            params: {
                order_id: orderID,
                new_status: new_status
            },
            headers: { Authorization: `Bearer ${access_token}` }
        })
}

export function updateOrderDeliverer(access_token, new_status, orderID) {
    return axios
        .post(`${server_addr}/deliverer/order/update`,
            null, {
            params: {
                order_id: orderID,
                new_status: new_status
            },
            headers: { Authorization: `Bearer ${access_token}` }
        })
}