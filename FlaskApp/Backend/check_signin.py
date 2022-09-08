import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Datavase')
import constants, models
from constants import SIGNIN_EMAIL_FAIL, SIGNIN_EMAIL_SUCCESS,\
    SIGNIN_PASSWORD_FAIL, SIGNIN_PASSWORD_SUCCESS
from models import User


def check_email_signin(email):
    user = User.query.filter(User.email_address == email).first()

    if user:
        return user
    return SIGNIN_EMAIL_FAIL


def check_password_signin(user, password):
    if user.check_password(password):
        return user
    return SIGNIN_PASSWORD_FAIL
