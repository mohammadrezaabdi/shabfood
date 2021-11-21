import logging
import main
from model.schema import Food, Food_Status
from utils import is_name_valid
from fastapi import HTTPException, status
from model.exceptions import *


async def create_food(restaurant_id: str, food: Food):
    # check the name format
    if not is_name_valid(food.name):
        logging.info(f'create food({restaurant_id}) failed.\n  wrong name format')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='name format is invalid.')
    try:
        await main.db.get_restaurant(restaurant_id)  # check if restaurant exists
        await main.db.create_food(restaurant_id, food)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'create food({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='restaurant not found.')
    except DUPLICATE_ENTITY_EXCEPTION as e:
        logging.info(f'create food({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='there is a food with same id.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'create food({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'create food({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'create food({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='food not found.')


async def get_food(id: str) -> Food:
    try:
        return await main.db.get_food(id)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='food not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='food not found.')


async def get_menu(restaurant_id: str) -> list:
    try:
        await main.db.get_restaurant(restaurant_id)  # check if restaurant exists
        return await main.db.get_foods(restaurant_id)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'get menu({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='restaurant not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'get menu({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'get menu({restaurant_id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='food not found.')


async def update_food(restaurant_id: str, id: str, new_name: str, new_price: str, new_status: Food_Status):
    # check the name format
    if new_name is not None and not is_name_valid(new_name):
        logging.info(f'update food({id}) failed.\n  incorrect name')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='name format is invalid.')
    try:
        foods = [f.id for f in await main.db.get_foods(restaurant_id)]  # check if food is in restaurant
        food = await main.db.get_food(id)  # check if food exists
        if food.id not in foods:
            logging.info(f'update food({id}) failed.\n  food not found')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='food not found in restaurant\'s menu.')
        await main.db.update_food(id, new_name, new_price, new_status)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'update food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='food not found.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'update food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'update food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'update food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='food not found.')


async def delete_food(restaurant_id: str, id: str):
    try:
        foods = [f.id for f in await main.db.get_foods(restaurant_id)]  # check if food is in restaurant
        food = await main.db.get_food(id)  # check if food exists
        if food.id not in foods:
            logging.info(f'update food({id}) failed.\n  food not found')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='food not found in restaurant\'s menu.')
        await main.db.delete_food(id)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'delete food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='food not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'delete food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'delete food({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='food not found.')
