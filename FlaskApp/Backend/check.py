import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
import constants, check_signup, check_signin, check_privateoffice, check_query
from constants import *
from check_signup import check_email_signup, check_password_signup
from check_signin import check_email_signin, check_password_signin
from check_privateoffice import check_name_spell, check_lastname_spell, check_date, check_address
from check_query import check_query_name_spell, check_description_spell, check_sql_query


def check_signin(email, password):
    ret = check_email_signin(email)

    if ret == SIGNIN_EMAIL_FAIL:
        return SIGNIN_EMAIL_FAIL #'Такая учетная запись CovidMonitoring не существует.
                                # Введите другую учетную запись или зарегистрируйте новую'

    if check_password_signin(ret, password) == SIGNIN_PASSWORD_FAIL:
        return SIGNIN_PASSWORD_FAIL #Пароль не верен. Введите корректный пароль

    return ret


def check_signup_email(email):
    return check_email_signup(email)


def check_signup_password(password):
    return check_password_signup(password)


def check_private_office(name, lastname, day, month, year, address):

    ret = check_name_spell(name)
    if ret:
        return ret

    ret = check_lastname_spell(lastname)
    if ret:
        return ret

    ret = check_date(day, month, year)
    if ret:
        return ret

    ret = check_address(address)

    return ret


def check_query(name, description, sql_query):

    ret = check_query_name_spell(name)
    if ret:
        return ret

    ret = check_description_spell(description)
    if ret:
        return ret

    ret = check_sql_query(sql_query)
    if ret:
        return ret

    return ret
