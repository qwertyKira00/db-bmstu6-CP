import psycopg2
import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
import constants

from constants import PSYCOPG2_ERROR, PSYCOPG2_SUCCESS, SQL_ERROR


def init_con():
    try:
        con = psycopg2.connect(
            database="postgres",
            user="kira",
            password="password",
            host="127.0.0.1",
            port="5432")
    except:
        return PSYCOPG2_ERROR

    cur = con.cursor()
    return cur, con


def sql_query_execute(sql_query):
    cur, con = init_con()
    if cur == PSYCOPG2_ERROR:
        return PSYCOPG2_ERROR

    try:
        cur.execute(sql_query)
    except:
        return SQL_ERROR

    try:
        con.commit()
    except:
        return PSYCOPG2_ERROR

    con.close()

    return PSYCOPG2_SUCCESS


def sql_execute_output(sql_query):
    cur, con = init_con()
    if cur == PSYCOPG2_ERROR:
        return PSYCOPG2_ERROR

    try:
        cur.execute(sql_query)
        rows = cur.fetchall()
    except:
        return SQL_ERROR

    return rows