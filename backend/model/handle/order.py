import logging
import random
from typing import List
import main
from model.schema import *
from utils import format_phone_number, get_current_time
from fastapi import HTTPException, status
from model.exceptions import *
from model.schema import *


async def create_order(customer_id: str, restaurant_id: str, items: List[Order_item]):
    # Normalizing phonenumber
    try:
        customer_id = format_phone_number(customer_id)
    except Exception as e:
        logging.info(f'get customer current orders({customer_id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')
    try:
        # check if food is in restaurant
        foods = [f.id for f in await main.db.get_foods(restaurant_id)]
        # Validating each item
        for item in items:
            # Check if food exists
            food = await main.db.get_food(item.food_id)
            if food.id not in foods:
                logging.info(f'update food({food.id}) failed.\n  food not found')
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail='food not found in restaurant\'s menu.')
            # Validating the availability of food
            if food.status == Food_Status.UNAVAILABLE:
                logging.info(f'create order failed.\n food is unavailable ({food.id})')
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='at least one food is unavailable.')
            # Validating quantity
            if item.quantity <= 0:
                logging.info(f'create order failed.\n  wrong quantity for food ({food.id})')
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='quantity of at least one food is not positive.')

        customer = await main.db.get_customer(customer_id)  # check if customer exists
        restaurant = await main.db.get_restaurant(restaurant_id)  # check if restaurant exists
        await main.db.create_order(
            Order(customer=customer, restaurant=restaurant, timestamp=get_current_time(),
                  status=Order_Status.RESTAURANT_PENDING, items=items))
    except ENTITY_NOT_FOUND as e:
        logging.info(f'create order failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='restaurant or customer not found.')
    except DUPLICATE_ENTITY_EXCEPTION as e:
        logging.info(f'create order failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='there is a order with same id.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'create order failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'create order failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'create order failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='something happened at backend.')


async def get_customer_current_orders(customer_id: str) -> List[Order]:
    try:
        try:
            customer_id = format_phone_number(customer_id)
        except Exception as e:
            logging.info(f'get customer current orders({customer_id}) failed.\n  {str(e)}')
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')
        await main.db.get_customer(customer_id)  # check if customer exists
        return await main.db.get_orders(status=get_set_of_current_status_customer(), customer_id=customer_id)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get current orders of customer({customer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='customer not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get current orders of customer({customer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get current orders of customer({customer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def get_customer_order(customer_id: str, order_id: str) -> Order:
    try:
        try:
            customer_id = format_phone_number(customer_id)
        except Exception as e:
            logging.info(f'get customer order({order_id}) failed.\n  {str(e)}')
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')

        await main.db.get_customer(customer_id)  # check if customer exists
        candid_order = await main.db.get_order(order_id)  # check if order exists
        # TODO: I'm not sure whether this 'if' block is necessary.
        if candid_order.customer.id != customer_id:
            logging.info(f'get order({order_id}) failed.\n claimed customer does not own order.')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='this order is not yours.')
        return candid_order
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='order or customer not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='something happened at backend.')


async def update_order_restaurant(order_id: str, restaurant_id: str, new_status: Order_Status):
    # TODO: Cancellation has not yet been implemented.
    try:
        await main.db.get_restaurant(restaurant_id)  # check if restaurant exists
        order = await main.db.get_order(order_id)  # check if order exists
        # TODO: I'm not sure whether this 'if' block is necessary.
        if order.restaurant.id != restaurant_id:
            logging.info(f'get order({order_id}) failed.\n claimed restaurant does not own order.')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='this order is not yours.')

        # Validating the status transition
        cur_status = order.status
        if not (cur_status, new_status) in valid_order_status_transitions_restaurant():
            logging.info(f'update order({order_id}) failed.\n  incorrect new status')
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='new status to update order is invalid.')

        if new_status == Order_Status.DELIVERER_PENDING and order.deliverer is None:
            # find all deliverers with IDLE status
            idle_deliverers = [d.id for d in await main.db.get_deliverers(Deliverer_Status.IDLE)]
            # pick one deliverer randomly and suggest him/her this order
            if not idle_deliverers:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail='no idle deliverer found.')
            candid_idle_deliverer_id = random.choice(idle_deliverers)
            await main.db.update_order(order_id=order_id, new_status=new_status,
                                       new_deliverer_id=candid_idle_deliverer_id)
            await main.db.update_deliverer(id=candid_idle_deliverer_id, new_status=Deliverer_Status.ON_DECISION)
        else:
            await main.db.update_order(order_id=order_id, new_status=new_status)

    except ENTITY_NOT_FOUND as e:
        logging.info(f'update order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='order or restaurant not found.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'update order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'update order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'update order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='order not found.')


async def get_restaurant_current_orders(restaurant_id: str) -> List[Order]:
    try:
        await main.db.get_restaurant(restaurant_id)  # check if restaurant exists
        return await main.db.get_orders(status=get_set_of_current_status_restaurant(), restaurant_id=restaurant_id)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get current orders of restaurant({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='restaurant not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get current orders of restaurant({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get current orders of restaurant({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def get_restaurant_order(restaurant_id: str, order_id: str) -> Order:
    try:
        await main.db.get_restaurant(restaurant_id)  # check if restaurant exists
        candid_order = await main.db.get_order(order_id)  # check if order exists
        # TODO: I'm not sure whether this 'if' block is necessary.
        if candid_order.restaurant.id != restaurant_id:
            logging.info(f'get order({order_id}) failed.\n claimed restaurant does not own order.')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='this order is not yours.')
        return candid_order
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='order or restaurant not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='something happened at backend.')


async def update_order_deliverer(order_id: str, deliverer_id: str, new_status: Order_Status):
    # TODO: Cancellation has not been implemented yet.
    # Validating the status transition
    order = await main.db.get_order(order_id=order_id)
    cur_status = order.status
    if not (cur_status, new_status) in valid_order_status_transitions_deliverer():
        logging.info(f'update order({order_id}) failed.\n  incorrect new status')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='new status to update order is invalid.')

    try:
        try:
            deliverer_id = format_phone_number(deliverer_id)
        except Exception as e:
            logging.info(f'update order({order_id}) failed.\n  {str(e)}')
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')

        await main.db.get_deliverer(deliverer_id)  # check if deliverer exists
        if new_status == Order_Status.DELIVERER_PENDING:  # Candid deliverer rejects the order suggestion
            # find all deliverers with IDLE status
            idle_deliverers = [d.id for d in await main.db.get_deliverers(Deliverer_Status.IDLE)]
            # pick one deliverer randomly and suggest him/her this order
            if idle_deliverers:
                candid_idle_deliverer_id = random.choice(idle_deliverers)
                await main.db.update_deliverer(id=candid_idle_deliverer_id, new_status=Deliverer_Status.ON_DECISION)
                await main.db.update_order(order_id=order_id, new_status=new_status,
                                           new_deliverer_id=candid_idle_deliverer_id)
            else:
                await main.db.update_order(order_id=order_id, new_status=new_status, new_deliverer_id='NULL')
            await main.db.update_deliverer(id=deliverer_id,
                                           new_status=Deliverer_Status.IDLE)  # change the status of rejecter deliverer back to IDLE
            return
        elif new_status == Order_Status.DELIVERING:
            await main.db.update_deliverer(id=deliverer_id, new_status=Deliverer_Status.BUSY)
        elif new_status in [Order_Status.CANCEL, Order_Status.DONE]:
            await main.db.update_deliverer(id=deliverer_id, new_status=Deliverer_Status.IDLE)
        await main.db.update_order(order_id=order_id, new_status=new_status)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'update order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='order or restaurant not found.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'update order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'update order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'update order({order_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='order not found.')


async def get_deliverer_current_order(deliverer_id: str) -> Order:
    try:
        try:
            deliverer_id = format_phone_number(deliverer_id)
        except Exception as e:
            logging.info(f'get current order of deliverer({deliverer_id}) failed.\n  {str(e)}')
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')

        await main.db.get_deliverer(deliverer_id)  # check if deliverer exists
        orders = await main.db.get_orders(status=get_set_of_current_status_deliverer(), deliverer_id=deliverer_id)
        if orders:
            return orders[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='you do not have any ongoing orders.')
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get current order of deliverer({deliverer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='deliverer not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get current order of deliverer({deliverer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get current order of deliverer({deliverer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def get_deliverer_suggested_order(deliverer_id: str) -> Order:
    try:
        try:
            deliverer_id = format_phone_number(deliverer_id)
        except Exception as e:
            logging.info(f'get current order of deliverer({deliverer_id}) failed.\n  {str(e)}')
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')

        deliverer = await main.db.get_deliverer(deliverer_id)  # check if deliverer exists
        orders = await main.db.get_orders(status=[Order_Status.DELIVERER_PENDING], deliverer_id=deliverer_id)
        if deliverer.status == Deliverer_Status.ON_DECISION and orders:
            return orders[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='you do not have any suggested orders currently.')
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get current order of deliverer({deliverer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='deliverer not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get current order of deliverer({deliverer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get current order of deliverer({deliverer_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')
