import logging
import main
from fastapi import HTTPException, status
from utils import check_password, format_phone_number, is_password_valid
from model.exceptions import *
from model.schema import Customer


async def create_customer(customer: Customer):
    # normalize phone number to E164
    try:
        customer.id = format_phone_number(customer.id)
    except Exception as e:
        logging.info(f'signup customer({customer.id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')
    # check the strength of password
    if not is_password_valid(customer.password):
        logging.info(f'signup customer({customer.id}) failed.\n  weak password')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='password is weak, it should has a minimum of 6 characters, at least 1 uppercase letter, 1 lowercase letter, and 1 number with no spaces.')
    try:
        await main.db.create_customer(customer)
    except DUPLICATE_ENTITY_EXCEPTION as e:
        logging.info(f'signup customer({customer.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='there is a customer with same phone number.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'signup customer({customer.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'signup customer({customer.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'signup customer({customer.id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def authenticate_customer(id: str, password: str):
    # normalize phone number to E164
    try:
        id = format_phone_number(id)
    except Exception as e:
        logging.info(f'signin customer({id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')
    try:
        # authenticate the user with password
        customer = await main.db.get_customer(id)
        if not check_password(password, customer.password):
            logging.info(f'signin customer({id}) failed.\n  wrong password.')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='password is not correct.')
    except ENTITY_NOT_FOUND as e:
        logging.info(f'signin customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='customer not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'signin customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'signin customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def update_customer(id: str, new_id: str, new_password: str, new_address: str):
    # normalize phone number to E164
    try:
        if new_id is not None:
            new_id = format_phone_number(new_id)
        id = format_phone_number(id)
    except Exception as e:
        logging.info(f'update customer({id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='phone number is not acceptable.')
    # check the strength of password
    if new_password is not None and not is_password_valid(new_password):
        logging.info(f'update customer({id}) failed.\n  weak password')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='password is weak, it should has a minimum of 6 characters, at least 1 uppercase letter, 1 lowercase letter, and 1 number with no spaces.')
    try:
        await main.db.get_customer(id)  # check if customer exists
        await main.db.update_customer(id, new_id, new_password, new_address)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'update customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='customer not found.')
    except DUPLICATE_ENTITY_EXCEPTION as e:
        logging.info(f'update customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='there is a customer with same phone number.')
    except FIELD_REGEX_FAILED as e:
        logging.info(f'update customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    except SYNTAX_ERROR as e:
        logging.info(f'update customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'update customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')


async def delete_customer(id: str):
    # normalize phone number to E164
    try:
        id = format_phone_number(id)
    except Exception as e:
        logging.info(f'delete customer({id}) failed.\n  {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='value is not acceptable.')
    try:
        await main.db.get_customer(id)  # check if customer exists
        await main.db.delete_customer(id)
    except ENTITY_NOT_FOUND as e:
        logging.info(f'delete customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='customer not found.')
    except SYNTAX_ERROR as e:
        logging.info(f'delete customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='request is not correct.')
    except INTERNAL_DATABASE_ERROR as e:
        logging.info(f'delete customer({id}) failed.\n  {e.message}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='something happened at backend.')
