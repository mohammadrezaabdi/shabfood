import logging
import main
from fastapi import HTTPException, status
from utils import check_password, is_email_valid, is_password_valid, is_name_valid
from model.exceptions import *
from model.schema import Restaurant, Order


async def create_restaurant(restaurant: Restaurant):
    # validating the email address
    if not is_email_valid(restaurant.id):
        logging.info(f'signup restaurant({restaurant.id}) failed.\n  wrong email format')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='please enter a valid email address.')
    # validating name
    if not is_name_valid(restaurant.name):
        logging.info(f'create restaurant({restaurant.id}) failed.\n  wrong name format')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='name format is invalid.')
    # check the strength of password
    if not is_password_valid(restaurant.password):
        logging.info(f'signup restaurant({restaurant.id}) failed.\n  weak password')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='password is weak, it should has a minimum of 6 characters, at least 1 uppercase letter, 1 lowercase letter, and 1 number with no spaces.')
    # TODO: No formatting has been checked for the address of restaurant nor customer. It is needed?
    try:
        await main.db.create_restaurant(restaurant)
    except DUPLICATE_ENTITY_EXCEPTION as e:
        logging.info(f'signup restaurant({restaurant.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='there is a restaurant with same email address.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'signup restaurant({restaurant.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'signup restaurant({restaurant.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'signup restaurant({restaurant.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def authenticate_restaurant(id: str, password: str):
    # validating the email address
    if not is_email_valid(id):
        logging.info(f'signin restaurant({id}) failed.\n  wrong email format')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='please enter a valid email address.')
    try:
        # authenticate the user with password
        restaurant = await main.db.get_restaurant(id)
        if not check_password(password, restaurant.password):
            logging.info(f'signin restaurant({id}) failed.\n  wrong password.')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='password is not correct.')
    except ENTITY_NOT_FOUND as e:
        logging.info(f'signin restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='restaurant not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'signin restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'signin restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def update_restaurant(id: str, new_id: str, new_password: str, new_name: str, new_address: str):
    # validating the email address
    if not is_email_valid(id):
        logging.info(f'signin restaurant({id}) failed.\n  wrong email format')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='please enter a valid email address.')
    # check the strength of password
    if new_password is not None and not is_password_valid(new_password):
        logging.info(f'update deliverer({id}) failed.\n  weak password')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='password is weak, it should has a minimum of 6 characters, at least 1 uppercase letter, 1 lowercase letter, and 1 number with no spaces.')
    # validating name
    if new_name is not None and not is_name_valid(new_name):
        logging.info(f'update restaurant({id}) failed.\n  wrong name format')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='name format is invalid.')
    try:
        await main.db.get_restaurant(id)  # check if restaurant exists
        await main.db.update_restaurant(id, new_id, new_password, new_name, new_address)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'update restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='restaurant not found.')
    except DUPLICATE_ENTITY_EXCEPTION as e:
        logging.info(f'update restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='there is a restaurant with same email address.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'update restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'update restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'update restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def delete_restaurant(id: str):
    # validating the email address
    if not is_email_valid(id):
        logging.info(f'delete restaurant({id}) failed.\n  wrong email format')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='please enter a valid email address.')
    try:
        await main.db.get_restaurant(id)  # check if restaurant exists
        await main.db.delete_restaurant(id)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'delete restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='restaurant not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'delete restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'delete restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def get_restaurant_public(id: str):
    # validating the email address
    if not is_email_valid(id):
        logging.info(f'get restaurant({id}) failed.\n  wrong email format')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='please enter a valid email address.')
    try:
        restaurant = await main.db.get_restaurant(id)
        restaurant.menu = await main.db.get_foods(restaurant.id)
        restaurant.password = None
        return restaurant
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='restaurant not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get restaurant({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def get_all_restaurants():
    try:
        restaurants = await main.db.get_all_restaurants()
        for r in restaurants:
            r.password = None
        return restaurants
    except ENTITY_NOT_FOUND as e:
        logging.info(f'no restaurant found.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='no restaurant was found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get all restaurants failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get all restaurants failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')
