from flask import flash, render_template, redirect, url_for, request, Blueprint
from flask_login import login_user, logout_user, login_required
from flask_security import roles_accepted, roles_required
import yagmail

import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Database')
import check, constants, signup_code, query, sql_execute, models
from check import *
from constants import *
from signup_code import *
from query import *
from sql_execute import *
from models import *

email_code = {}

main = Blueprint('main', __name__)


@main.route('/') #отслеживание главной страницы
@main.route('/home')
def index():
    return render_template("index.html")


@main.route('/database', methods=['POST', 'GET'])
def database():

    if request.method == 'POST':
        if request.form['submit_button'] == 'patients':
            person = Person.query.all()
            return render_template("database.html", person=person, id = 1)

        if request.form['submit_button'] == 'location':
            location = Location.query.all()
            return render_template("database.html", location=location, id=2)

        if request.form['submit_button'] == 'status':
            status = Status.query.all()
            return render_template("database.html", status=status, id=3)

        if request.form['submit_button'] == 'symptoms':
            symptom = Symptom.query.all()
            return render_template("database.html", symptom=symptom, id=4)

        if request.form['submit_button'] == 'ps':
            person_symptom =db.session.query(PersonSymptom)
            return render_template("database.html", person_symptom=person_symptom, id=5)

        if request.form['submit_button'] == 'diagram':
            return render_template("database.html", id=6)

        if request.form['submit_button'] == 'hide':
            return render_template("database.html")

        if request.form['submit_button'] == 'sql':
            sql_query = request.form['sql_query']
            ret = sql_query_execute(sql_query)
            if ret != PSYCOPG2_SUCCESS:
                error = errors[str(ret)]
                return render_template("database.html", error=error)
            else:
                flash('Запрос успешно выполнен')

    return render_template("database.html")


@main.route('/signup_email', methods=['POST', 'GET'])
def signup_email():
    error = None

    if request.method == 'POST':
        email_address = request.form['email']

        ret = check_signup_email(email_address)
        if ret != SIGNUP_EMAIL_SUCCESS:
            error = email_address + errors[str(ret)]
        else:
            email_code[email_address] = None
            return redirect(url_for('.signup_password', email_address=email_address))

    return render_template("signup_email.html", error=error)


@main.route('/signup_password/<string:email_address>', methods=['POST', 'GET'])
def signup_password(email_address):
    error = None

    if request.method == 'POST':
        password = request.form['password']

        if check_signup_email(email_address):
            return redirect(url_for('.signup_code', email_address=email_address, password=password))

        ret = check_signup_password(password)
        if ret != SIGNUP_PASSWORD_SUCCESS:
            error = errors[str(ret)]
        else:
            return redirect(url_for('.signup_code', email_address=email_address, password=password))

    return render_template("signup_password.html", email_address=email_address, error=error)


@main.route('/signup_code/<string:email_address>/<string:password>', methods=['POST', 'GET'])
def signup_code(email_address, password):
    error = None

    if request.method == 'GET' and not email_code[email_address]:
        email_code[email_address] = code_generate()
        content = EMAIL_TEXT_PREV + \
            email_code[email_address] + \
            EMAIL_TEXT_POST + \
            EMAIL_TEXT_SIGNATURE

        yagmail.SMTP(SERVER_EMAIL).send(email_address, SUBJECT, content)

    if request.method == 'POST':
        code = request.form['code']

        if code != email_code[email_address]:
            error = errors[str(CODE_FAIL)]
        else:
            return redirect(url_for('.create_privateoffice', email_address=email_address, password=password))

    return render_template("signup_code.html", email_address=email_address, error=error)


@main.route('/privateoffice/<string:email_address>/<string:password>', methods=['POST', 'GET'])
def create_privateoffice(email_address, password):
    error = None

    if request.method == 'POST':
        name = request.form['firstName']
        lastname = request.form['lastName']
        day_of_birth = request.form['Day']
        month_of_birth = request.form['Month']
        year_of_birth = request.form['Year']
        gender = request.form['Gender']
        address = request.form['address']
        health_status = request.form['HealthStatus']
        role = request.form['Role']

        ret = check_private_office(name, lastname, day_of_birth, month_of_birth, year_of_birth, address)
        if ret != PRIVATE_OFFICE_SUCCESS:
            error = errors[str(ret)]
        else:
            ret = add_new_user(email_address, password, role)
            if ret != NEW_USER_ADD_SUCCESS:
                error = errors[str(ret)]
            else:
                ret = add_new_privateoffice(email_address,
                    name,
                    lastname,
                    day_of_birth,
                    month_of_birth,
                    year_of_birth,
                    gender,
                    address,
                    health_status)
                if ret == NEW_PRIVATE_OFFICE_ADD_SUCCESS:
                    flash('Учетная запись CovidMonitoring успешно создана')
                    return redirect('/')
                else:
                    error = errors[str(ret)]

    return render_template("privateoffice.html", email_address=email_address, error=error)


@main.route('/privateoffice_page', methods = ['POST', 'GET'])
@login_required
def privateoffice_page():
    q = PrivateOffice.query.join(User).filter(User.id==current_user.id).first()
    month = get_month(q.month_of_birth)

    health_status = q.health_status

    if request.method == 'POST':
        health_status = request.form['HealthStatus']

    update_privateoffice(int(health_status))

    percentage = round(q.addr.infected / q.addr.population * 100, 2)

    return render_template("privateoffice_page.html", name=q.name, lastname=q.lastname, gender=q.gender,
                           day=q.day_of_birth, month=month, year=q.year_of_birth,
                           address=q.address, health_status=int(health_status), percentage=percentage)


@main.route('/authorization', methods = ['POST', 'GET'])
def sign_in():
    error = None

    if request.method == 'POST':
        email_address = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember-me') else False

        ret = check_signin(email_address, password)
        if ret == SIGNIN_EMAIL_FAIL or ret == SIGNIN_PASSWORD_FAIL:
            error = errors[str(ret)]
        else:
            flash('Авторизация успешна')
            login_user(ret, remember=remember)
            return redirect('/')

    return render_template("authorization.html", error=error)


@main.route('/query', methods = ['POST', 'GET'])
@roles_accepted('user', 'specialist')
def query():

    query_list = Query.query.all()

    if request.method == 'POST':
        query = request.form['listGroupCheckableRadios']

        if query == "quantityByStatus":
            res = get_qty_by_status()
            return render_template("query.html", query_list=query_list, query_number=1, res=res)

        if query == "deathQuantityByCountry":
            res = get_DeathQty_by_country()
            return render_template("query.html", query_list=query_list, query_number=2, res=res)

        if query == "desc1" or query == "asc1":
            res = get_DeathQty_by_country_ordered(query)
            return render_template("query.html", query_list=query_list, query_number=2, res=res)

        if query == "recQuantityByCountry":
            res = get_RecQty_by_country()
            return render_template("query.html", query_list=query_list, query_number=3, res=res)

        if query == "desc2" or query == "asc2":
            res = get_RecQty_by_country_ordered(query)
            return render_template("query.html", query_list=query_list, query_number=3, res=res)

        if query == "avgAgeByCountry":
            from decimal import Decimal
            res = get_avg_DeathAge_by_country()
            round_res = []
            for i in range(len(res)):
                round_res.append([])
                round_res[i].append(res[i][0])
                if res[i][1] == None:
                    round_res[i].append(res[i][1])
                else:
                    round_res[i].append(res[i][1].quantize(Decimal("1")))

            return render_template("query.html", query_list=query_list, query_number=4, res=round_res)

        if query == "desc3" or query == "asc3":
            from decimal import Decimal
            res = get_avg_DeathAge_by_country_ordered(query)
            round_res = []
            for i in range(len(res)):
                round_res.append([])
                round_res[i].append(res[i][0])
                if res[i][1] == None:
                    round_res[i].append(res[i][1])
                else:
                    round_res[i].append(res[i][1].quantize(Decimal("1")))

            return render_template("query.html", query_list=query_list, query_number=4, res=round_res)

        if query == "topSymptom":
            res = get_5top_symptom()
            return render_template("query.html", query_list=query_list, query_number=5, res=res)

        if query == "maxExpStart":
            res = get_max_exp_start()
            return render_template("query.html", query_list=query_list, query_number=6, res=res)

        if query == 'deathSymptom':
            res = get_death_symptom()
            return render_template("query.html", query_list=query_list, query_number=7, res=res)

        if query:
            for q in query_list:
                if q.name == query:
                    res = sql_execute_output(q.sql_query)
                    columns_name = q.columns_name.split(";")
            return render_template("query.html", query_list=query_list, query_number=8, res=res, columns_name=columns_name)

    return render_template("query.html", query_list=query_list)


@main.route('/create_query', methods = ['POST', 'GET'])
@roles_required('specialist')
def create_query():
    error = None

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        sql_query = request.form['sql_query']
        columns_name = request.form['columns_name']

        ret = check_query(name, description, sql_query)
        if ret != CREATE_QUERY_SUCCESS:
            error = errors[str(ret)]
        else:
            ret = add_new_query(name, description, sql_query, columns_name)
            if ret != NEW_QUERY_ADD_SUCCESS:
                error = errors[str(ret)]
            else:
                flash('Запрос успешно создан')
                return redirect('/query')

    return render_template("create_query.html", error=error)


@main.route('/logout', methods = ['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect('/')

