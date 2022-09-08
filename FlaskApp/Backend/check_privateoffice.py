import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
import constants
from constants import NAME_EMPTY_FAIL, NAME_SUCCESS, LASTNAME_EMPTY_FAIL, \
    LASTNAME_SUCCESS, DATE_INVALID, DATE_SUCCESS, ADDRESS_INVALID, ADDRESS_SUCCESS


def check_name_spell(name):
    if not name:
        return NAME_EMPTY_FAIL
    return NAME_SUCCESS


def check_lastname_spell(lastname):
    if not lastname:
        return LASTNAME_EMPTY_FAIL
    return LASTNAME_SUCCESS


def check_date(day, month, year):
    if not day.isdigit() or not year.isdigit() or not month:
        return DATE_INVALID

    day = int(day)
    if day < 0 or day > 31:
        return DATE_INVALID

    year = int(year)

    if year < 1910 or year > 2021:
        return DATE_INVALID

    if not (year % 4 == 0 and year % 100 != 0 or year % 400 == 0) and month == 'Февраль' and day > 28:
        return DATE_INVALID

    return DATE_SUCCESS


def check_address(address):
    if not address:
        return ADDRESS_INVALID
    return ADDRESS_SUCCESS
