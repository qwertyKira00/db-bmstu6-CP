import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Datavase')
import constants, sql_execute
from constants import QUERY_NAME_SUCCESS, QUERY_NAME_FAIL, \
    QUERY_DESCRIPTION_SUCCESS, QUERY_DESCRIPTION_FAIL, \
    SQL_SUCCESS, SQL_ERROR

from sql_execute import sql_query_execute


def check_query_name_spell(name):
    if not name:
        return QUERY_NAME_FAIL
    return QUERY_NAME_SUCCESS


def check_description_spell(description):
    if not description:
        return QUERY_DESCRIPTION_FAIL
    return QUERY_DESCRIPTION_SUCCESS


def check_sql_query(sql_query):
    if not sql_query:
        return SQL_ERROR
    return sql_query_execute(sql_query)
