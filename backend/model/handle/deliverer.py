import logging
import main
from fastapi import HTTPException, status
from utils import check_password, format_phone_number, is_password_valid
from model.exceptions import *
from model.schema import Deliverer, Deliverer_Status


async def create_deliverer(deliverer: Deliverer):
    # normalize phone number to E164
    try:
        deliverer.id = format_phone_number(deliverer.id)
    except Exception as e:
        logging.info(f'signup deliverer({deliverer.id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')
    # check the strength of password
    if not is_password_valid(deliverer.password):
        logging.info(f'signup deliverer({deliverer.id}) failed.\n  weak password')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='password is weak, it should has a minimum of 6 characters, at least 1 uppercase letter, 1 lowercase letter, and 1 number with no spaces.')
    try:
        await main.db.create_deliverer(deliverer)
    except DUPLICATE_ENTITY_EXCEPTION as e:
        logging.info(f'signup deliverer({deliverer.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='there is a deliverer with same phone number.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'signup deliverer({deliverer.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'signup deliverer({deliverer.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'signup deliverer({deliverer.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def authenticate_deliverer(id: str, password: str):
    # normalize phone number to E164
    try:
        id = format_phone_number(id)
    except Exception as e:
        logging.info(f'signin deliverer({id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')
    try:
        # authenticate the user with password
        deliverer = await main.db.get_deliverer(id)
        if not check_password(password, deliverer.password):
            logging.info(f'signin deliverer({id}) failed.\n  wrong password.')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='password is not correct.')
    except ENTITY_NOT_FOUND as e:
        logging.info(f'signin deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='deliverer not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'signin deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'signin deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def update_deliverer(id: str, new_id: str, new_password: str, new_status: Deliverer_Status):
    # normalize phone number to E164
    try:
        if new_id is not None:
            new_id.id = format_phone_number(new_id)
        id = format_phone_number(id)
    except Exception as e:
        logging.info(f'update deliverer({id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')
    # check the strength of password
    if new_password is not None and not is_password_valid(new_password):
        logging.info(f'update deliverer({id}) failed.\n  weak password')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='password is weak, it should has a minimum of 6 characters, at least 1 uppercase letter, 1 lowercase letter, and 1 number with no spaces.')
    try:
        await main.db.get_deliverer(id)  # check if deliverer exists
        await main.db.update_deliverer(id, new_id, new_password, new_status)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'update deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='deliverer not found.')
    except DUPLICATE_ENTITY_EXCEPTION as e:
        logging.info(f'update deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='there is a deliverer with same phone number.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'update deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'update deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'update deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def delete_deliverer(id: str):
    # normalize phone number to E164
    try:
        id = format_phone_number(id)
    except Exception as e:
        logging.info(f'delete deliverer({id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    try:
        await main.db.get_deliverer(id)  # check if deliverer exists
        await main.db.delete_deliverer(id)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'delete deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='deliverer not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'delete deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'delete deliverer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')
