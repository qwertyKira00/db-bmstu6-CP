import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp')
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
import __init__, constants
from __init__ import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_security import RoleMixin

from constants import NEW_USER_ADD_SUCCESS, NEW_USER_ADD_FAIL, \
    NEW_PRIVATE_OFFICE_ADD_SUCCESS, NEW_PRIVATE_OFFICE_ADD_FAIL,\
    UPDATE_PRIVATE_OFFICE_ADD_SUCCESS, UPDATE_PRIVATE_OFFICE_ADD_FAIL, \
    NEW_QUERY_ADD_SUCCESS, NEW_QUERY_ADD_FAIL


def add_new_user(email_address, password, role):
    users = User.query.all()
    id = users[len(users) - 1].id + 1
    user = User(id=id, email_address=email_address)
    user.set_password(password)

    user_role = Role.query.filter(Role.id == int(role)).first()
    user.roles.append(user_role)

    try:
        current_db_sessions = db.session.object_session(user)
        if current_db_sessions:
            current_db_sessions.add(user)
            current_db_sessions.commit()
        else:
            db.session.add(user)
            db.session.commit()
        return NEW_USER_ADD_SUCCESS
    except:
        return NEW_USER_ADD_FAIL


def add_new_privateoffice(email_address, name, lastname, day_of_birth, month_of_birth, year_of_birth, gender, address, health_status):
    user = User.query.filter(User.email_address == email_address).first()
    addr = Address.query.filter(Address.name == address).first()

    privateoffices = PrivateOffice.query.all()
    id = privateoffices[len(privateoffices) - 1].id + 1

    privateoffice = PrivateOffice(id=id, name=name, lastname=lastname, gender=gender,
                                  day_of_birth=int(day_of_birth), month_of_birth=month_of_birth,
                                  year_of_birth=int(year_of_birth), address=address, health_status=int(health_status),
                                  user=user, addr=addr)
    try:
        current_db_sessions = db.session.object_session(privateoffice)
        if current_db_sessions:
            current_db_sessions.add(privateoffice)
            current_db_sessions.commit()
        else:
            db.session.add(privateoffice)
            db.session.commit()
        return NEW_PRIVATE_OFFICE_ADD_SUCCESS
    except:
        return NEW_PRIVATE_OFFICE_ADD_FAIL


def update_privateoffice(health_status):

    privateoffice = PrivateOffice.query.filter(PrivateOffice.id_user == current_user.id).first()

    try:
        current_db_sessions = db.session.object_session(privateoffice)
        if current_db_sessions:
            privateoffice.health_status = health_status
            current_db_sessions.commit()
        else:
            db.session.commit()
        return UPDATE_PRIVATE_OFFICE_ADD_SUCCESS
    except:
        return UPDATE_PRIVATE_OFFICE_ADD_FAIL


def add_new_query(name, description, sql_query, columns_name):

    queries = Query.query.all()
    id = queries[len(queries) - 1].id + 1

    query = Query(id=id,
                  name=name,
                  description=description,
                  sql_query=sql_query,
                  columns_name=columns_name)

    try:
        current_db_sessions = db.session.object_session(query)
        if current_db_sessions:
            current_db_sessions.add(query)
            current_db_sessions.commit()
        else:
            db.session.add(query)
            db.session.commit()
        return NEW_QUERY_ADD_SUCCESS
    except:
        return NEW_QUERY_ADD_FAIL


users_roles = db.Table(
    'users_roles',
    db.Column('id_user', db.Integer(), db.ForeignKey('server_data.users.id')),
    db.Column('id_role', db.Integer(), db.ForeignKey('server_data.roles.id')),
    schema='server_data'
)


class Role(db.Model, RoleMixin):
    __table_args__ = {"schema": "server_data"}
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __table_args__ = {"schema": "server_data"}
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(100), unique=False)
    private_office = db.relationship('PrivateOffice',
                                     backref='user',
                                     uselist=False)
    roles = db.relationship('Role',
                            secondary=users_roles,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})


PersonSymptom = db.Table('person_symptom',
    db.Column('id_person', db.Integer, db.ForeignKey('public._person.id')),
    db.Column('id_symptom', db.Integer, db.ForeignKey('public._symptom.id')))


class PrivateOffice(db.Model):
    __table_args__ = {"schema": "server_data"}
    __tablename__ = "private_office"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    lastname = db.Column(db.String(20), unique=False)
    gender = db.Column(db.String(20), unique=False)
    day_of_birth = db.Column(db.Integer, unique=False)
    month_of_birth = db.Column(db.String(20), unique=False)
    year_of_birth = db.Column(db.Integer, unique=False)
    address = db.Column(db.String(64), unique=False)
    health_status = db.Column(db.Integer, unique=False)
    id_user = db.Column(db.Integer, db.ForeignKey('server_data.users.id'), nullable=False)
    id_address = db.Column(db.Integer, db.ForeignKey('server_data.address.id'), nullable=False)

    def __repr__(self):
        return '<PrivateOffice %r>' % self.id


class Query(db.Model):
    __table_args__ = {"schema": "server_data"}
    __tablename__ = "query"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255), unique=True)
    sql_query = db.Column(db.String(500), unique=True)
    columns_name = db.Column(db.String(255), unique=False)

    def __repr__(self):
        return '<Query %r>' % self.id


class Address(db.Model):
    __table_args__ = {"schema": "server_data"}
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    population = db.Column(db.Integer, unique=False)
    infected = db.Column(db.Integer, unique=False)
    pr_offices = db.relationship('PrivateOffice', backref='addr', lazy='dynamic')

    def __repr__(self):
        return '<Address %r>' % self.id


class Person(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = "_person"

    id = db.Column(db.Integer, primary_key=True)
    reporting_date = db.Column(db.String(10), unique=False)
    gender = db.Column(db.String(10), unique=False)
    age = db.Column(db.Integer, unique=False)
    symptom_onset = db.Column(db.String(10), unique=False)
    hosp_visit_date = db.Column(db.String(10), unique=False)
    exposure_start = db.Column(db.String(10), unique=False)
    exposure_end = db.Column(db.String(10), unique=False)
    visiting_wuhan = db.Column(db.Integer, unique=False) #bool
    from_wuhan = db.Column(db.Integer, unique=False)    #bool
    id_location = db.Column(db.Integer, db.ForeignKey('public._location.id'), nullable=False)
    id_status = db.Column(db.Integer, db.ForeignKey('public._status.id'), nullable=False)
    symptoms = db.relationship('Symptom', secondary=PersonSymptom,
                           backref=db.backref('people', lazy='dynamic'))

    def __init__(self, id, reporting_date, gender, age, symptom_onset, hosp_visit_date,
                 exposure_start, exposure_end, visiting_Wuhan, from_Wuhan, id_location, id_status):
        self.id = id
        self.reporting_date = reporting_date
        self.gender = gender
        self.age = age
        self.symptom_onset = symptom_onset
        self.hosp_visit_date = hosp_visit_date
        self.exposure_start = exposure_start
        self.exposure_end = exposure_end
        self.visiting_Wuhan = visiting_Wuhan
        self.from_Wuhan = from_Wuhan
        self.id_location = id_location
        self.id_status = id_status

    def __repr__(self):
        return '<Person %r>' % self.id


class Status(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = "_status"

    id = db.Column(db.Integer, primary_key=True)
    progress = db.Column(db.String(10), unique=True)
    people = db.relationship('Person', backref='status', lazy='dynamic')

    def __init__(self, id, progress):
        self.id = id
        self.progress = progress


    def __repr__(self):
        return '<Status %r>' % self.id


class Location(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = "_location"

    id = db.Column(db.Integer, primary_key=True)
    _location = db.Column(db.String(64), unique=False)
    country = db.Column(db.String(64), unique=False)
    latitude = db.Column(db.Float(7), unique=False)
    longitude =  db.Column(db.Float(7), unique=False)
    people = db.relationship('Person', backref='location', lazy='dynamic')

    def __init__(self, id, location, country, latitude, longitude):
        self.id = id
        self.location = location
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Location %r>' % self.id


class Symptom(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = "_symptom"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Symptom %r>' % self.id


def get_month(month):
    if month != 'Август':
        return (month.lower())[:len(month) - 1] + 'я'
    return month.lower() + 'а'