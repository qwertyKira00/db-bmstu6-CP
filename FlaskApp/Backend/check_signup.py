import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Datavase')
import constants, models
from constants import SIGNUP_EMAIL_FAIL, SIGNUP_EMAIL_EMPTY_FAIL, SIGNUP_EMAIL_SUCCESS, \
    SIGNUP_PASSWORD_LENGTH_FAIL, SIGNUP_PASSWORD_CONTENT_FAIL,\
    SIGNUP_PASSWORD_SUCCESS, PASSWORD_LENGTH
from models import User


def check_email_signup(email):
    if not email:
        return SIGNUP_EMAIL_EMPTY_FAIL

    users = User.query.all()

    for i in range(len(users)):
        if email == users[i].email_address:
            return SIGNUP_EMAIL_FAIL
    return SIGNUP_EMAIL_SUCCESS


def password_parse(password):
    is_upper, is_lower, is_digit = False, False, False

    for letter in password:
        if letter.isupper():
            is_upper = True
        if letter.islower():
            is_lower = True
        if letter.isdigit():
            is_digit = True

    if is_upper and is_lower and is_digit:
        return SIGNUP_PASSWORD_SUCCESS

    return SIGNUP_PASSWORD_CONTENT_FAIL


def check_password_signup(password):

    if not password or len(password) < PASSWORD_LENGTH:
        return SIGNUP_PASSWORD_LENGTH_FAIL

    return password_parse(password)

