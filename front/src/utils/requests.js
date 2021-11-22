import axios from 'axios'

const server_addr = "https://shabfood.darkube.app/api"

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
