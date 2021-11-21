import bcrypt
import re
import phonenumbers
import datetime


# define a singlethon class
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def message(message):
    return {'message': message}


def check_password(password, hash_password):
    """Check the password correction by its hashed one"""
    hash_password = hash_password.encode('utf-8')
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, hash_password) == hash_password


def format_phone_number(phone_number):
    """Format a phone number to E164 standard"""
    if phone_number[0] == '0':
        re.sub("^.", "", phone_number)
    return phonenumbers.format_number(phonenumbers.parse(phone_number, "IR"), phonenumbers.PhoneNumberFormat.E164)


def is_password_valid(password: str):
    """RULES
        + minimum of 6 characters
        + at least 1 uppercase letter
        + at least lowercase letter
        + at least 1 number
        + no spaces
    """
    return re.match(r'^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,})\S$', password)


def is_name_valid(name: str):
    """RULES
        + only alphanumeric characters, numbers, dash and underline
        + dash and underline can't be at the start of a name
    """
    return re.match(r'^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$', name)


def is_email_valid(email: str):
    # Reference: https://www.w3resource.com/javascript/form/email-validation.php
    return re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email)


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
