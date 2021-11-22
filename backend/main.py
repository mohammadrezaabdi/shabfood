import logging
import os
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth import create_token, JWTBearer, User_type
from model.handle.customer import *
from model.handle.deliverer import *
from model.handle.food import *
from model.handle.restaurant import *
from model.handle.order import *
from model.schema import *
from utils import message
from db.crud import Postgres_db

logging.basicConfig(format='%(levelname)s:%(funcName)s()\n   %(message)s',
                    level=logging.INFO, datefmt='%H:%M:%S')
app = FastAPI()
db = None

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    global db
    db = await Postgres_db.connect()


@app.on_event("shutdown")
async def shutdown():
    global db
    await db.disconnect()


############################ Customer ###############################################
@app.put("/customer/signup", tags=["customer"], status_code=status.HTTP_201_CREATED)
async def api_create_customer(customer: Customer):
    await create_customer(customer)
    return create_token(customer.id, User_type.customer)


@app.post("/customer/signin", tags=["customer"], status_code=status.HTTP_200_OK)
async def api_signin_customer(customer_id: str, password: str):
    await authenticate_customer(customer_id, password)
    return create_token(customer_id, User_type.customer)


@app.post("/customer/update", tags=["customer"], status_code=status.HTTP_202_ACCEPTED)
async def api_update_customer(new_id: str = None, new_password: str = None, new_address: str = None,
                              customer_id: str = Depends(JWTBearer(User_type.customer))):
    await update_customer(customer_id, new_id, new_password, new_address)
    return message('customer updated successfully.')


@app.delete("/customer/delete", tags=["customer"], status_code=status.HTTP_200_OK)
async def api_delete_customer(customer_id: str = Depends(JWTBearer(User_type.customer))):
    await delete_customer(customer_id)
    return message('customer deleted successfully.')


############################ Deliverer ###############################################
@app.put("/deliverer/signup", tags=["deliverer"], status_code=status.HTTP_201_CREATED)
async def api_create_deliverer(deliverer: Deliverer):
    await create_deliverer(deliverer)
    return create_token(deliverer.id, User_type.deliverer)


@app.post("/deliverer/signin", tags=["deliverer"], status_code=status.HTTP_200_OK)
async def api_signin_deliverer(deliverer_id: str, password: str):
    await authenticate_deliverer(deliverer_id, password)
    return create_token(deliverer_id, User_type.deliverer)


@app.post("/deliverer/update", tags=["deliverer"], status_code=status.HTTP_202_ACCEPTED)
async def api_update_deliverer(new_id: str = None, new_password: str = None, new_status: Deliverer_Status = None,
                               deliverer_id: str = Depends(JWTBearer(User_type.deliverer))):
    await update_deliverer(deliverer_id, new_id, new_password, new_status)
    return message('deliverer updated successfully.')


@app.delete("/deliverer/delete", tags=["deliverer"], status_code=status.HTTP_200_OK)
async def api_delete_deliverer(deliverer_id: str = Depends(JWTBearer(User_type.deliverer))):
    await delete_deliverer(deliverer_id)
    return message('deliverer deleted successfully.')


############################ Restaurant ###############################################
@app.put("/restaurant/signup", tags=["restaurant"], status_code=status.HTTP_201_CREATED)
async def api_create_restaurant(restaurant: Restaurant):
    await create_restaurant(restaurant)
    return create_token(restaurant.id, User_type.restaurant)


@app.post("/restaurant/signin", tags=["restaurant"], status_code=status.HTTP_200_OK)
async def api_signin_restaurant(restaurant_id: str, password: str):
    await authenticate_restaurant(restaurant_id, password)
    return create_token(restaurant_id, User_type.restaurant)


@app.post("/restaurant/update", tags=["restaurant"], status_code=status.HTTP_202_ACCEPTED)
async def api_update_restaurant(new_id: str = None, new_password: str = None, new_name: str = None,
                                new_address: str = None, restaurant_id: str = Depends(JWTBearer(User_type.restaurant))):
    await update_restaurant(restaurant_id, new_id, new_password, new_name, new_address)
    return message('restaurant updated successfully.')


@app.delete("/restaurant/delete", tags=["restaurant"], status_code=status.HTTP_200_OK)
async def api_deleteـrestaurant(restaurant_id: str = Depends(JWTBearer(User_type.restaurant))):
    await delete_restaurant(restaurant_id)
    return message('restaurant deleted successfully.')


@app.get("/restaurant/all", tags=["restaurant"], status_code=status.HTTP_200_OK)
async def api_get_all_restaurants():
    return await get_all_restaurants()


@app.get("/restaurant/{restaurant_id}", tags=["restaurant"], status_code=status.HTTP_200_OK)
async def api_get_restaurant(restaurant_id: str):
    # (restaurant, restaurant_foods) is returned by the following call where the second element is a list itself.
    return await get_restaurant_public(restaurant_id)


############################ Food ###############################################
@app.put("/restaurant/food/add", tags=["food"], status_code=status.HTTP_201_CREATED)
async def api_create_food(restaurant_id: str = Depends(JWTBearer(User_type.restaurant)), food: Food = None):
    await create_food(restaurant_id, food)
    return message('food created successfully.')


@app.post("/restaurant/food/update", tags=["food"], status_code=status.HTTP_202_ACCEPTED)
async def api_update_food(food_id: str, new_name: str = None, new_price: str = None, new_status: Food_Status = None,
                          restaurant_id: str = Depends(JWTBearer(User_type.restaurant))):
    await update_food(restaurant_id, food_id, new_name, new_price, new_status)
    return message('food updated successfully.')


@app.delete("/restaurant/food/delete", tags=["food"], status_code=status.HTTP_200_OK)
async def api_delete_food(food_id: str, restaurant_id: str = Depends(JWTBearer(User_type.restaurant))):
    await delete_food(restaurant_id, food_id)
    return message('food deleted successfully.')


@app.get("/restaurant/food/{food_id}", tags=["food"], status_code=status.HTTP_200_OK)
async def api_get_food(food_id: str):
    return await get_food(food_id)


@app.get("/restaurant/menu/{restaurant_id}", tags=["food"], status_code=status.HTTP_200_OK)
async def api_get_menu(restaurant_id: str):
    return await get_menu(restaurant_id)


############################ Order ###############################################
# Customer related
@app.put("/customer/order/create", tags=["order"], status_code=status.HTTP_201_CREATED)
async def api_create_order(restaurant_id: str, items: List[Order_item],
                           customer_id: str = Depends(JWTBearer(User_type.customer))):
    await create_order(customer_id, restaurant_id, items)
    return message('order created successfully.')


@app.get("/customer/order/currents", tags=["order"], status_code=status.HTTP_200_OK)
async def api_get_customer_current_orders(customer_id: str = Depends(JWTBearer(User_type.customer))):
    return await get_customer_current_orders(customer_id=customer_id)


@app.get("/customer/order/{order_id}", tags=["order"], status_code=status.HTTP_200_OK)
async def api_get_customer_order(order_id: str, customer_id: str = Depends(JWTBearer(User_type.customer))):
    return await get_customer_order(customer_id=customer_id, order_id=order_id)


# Restaurant related
@app.post("/restaurant/order/update", tags=["order"], status_code=status.HTTP_202_ACCEPTED)
async def api_update_order_restaurant(order_id: str, new_status: Order_Status,
                                      restaurant_id: str = Depends(JWTBearer(User_type.restaurant))):
    await update_order_restaurant(order_id, restaurant_id, new_status)
    return message("order was updated successfully.")


@app.get("/restaurant/order/currents", tags=["order"], status_code=status.HTTP_200_OK)
async def api_get_restaurant_current_orders(restaurant_id: str = Depends(JWTBearer(User_type.restaurant))):
    return await get_restaurant_current_orders(restaurant_id)


@app.get("/restaurant/order/{order_id}", tags=["order"], status_code=status.HTTP_200_OK)
async def api_get_restaurant_order(order_id: str, restaurant_id: str = Depends(JWTBearer(User_type.restaurant))):
    return await get_restaurant_order(restaurant_id=restaurant_id, order_id=order_id)


# Deliverer related
@app.post("/deliverer/order/update", tags=["order"], status_code=status.HTTP_202_ACCEPTED)
async def api_update_order_deliverer(order_id: str, new_status: Order_Status,
                                     deliverer_id: str = Depends(JWTBearer(User_type.deliverer))):
    await update_order_deliverer(order_id, deliverer_id, new_status)
    return message("order was updated successfully.")


@app.get("/deliverer/order/request", tags=["order"], status_code=status.HTTP_202_ACCEPTED)
async def api_get_deliverer_current_order(deliverer_id: str = Depends(JWTBearer(User_type.deliverer))):
    return await get_deliverer_suggested_order(deliverer_id=deliverer_id)


@app.get("/deliverer/order/current", tags=["order"], status_code=status.HTTP_202_ACCEPTED)
async def api_get_deliverer_current_order(deliverer_id: str = Depends(JWTBearer(User_type.deliverer))):
    return await get_deliverer_current_order(deliverer_id=deliverer_id)


if __name__ == "__main__":
    os.system("uvicorn main:app --host 0.0.0.0 --reload")
