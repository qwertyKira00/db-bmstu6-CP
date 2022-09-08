import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Datavase')
import models
from models import *

def get_qty_by_status():
    # Сгруппировать по статусу состояния здоровья
    quantityByStatus = db.session.query(Status.progress, db.func.count(Person.id)). \
        join(Status.people). \
        group_by(Status.progress). \
        all()
    return quantityByStatus


def get_DeathQty_by_country():
    # Получить количество умерших пациентов в каждой стране
    deathQuantityByCountry = db.session.query(Location.country, db.func.count(Person.id)). \
        join(Location.people). \
        filter(Person.id_status == 3). \
        group_by(Location.country). \
        all()
    return deathQuantityByCountry


def get_DeathQty_by_country_ordered(sort_type):
    # Получить количество умерших пациентов в каждой стране (сортированный)
    if sort_type == 'desc1':
        deathQuantityByCountry = db.session.query(Location.country, db.func.count(Person.id)). \
            join(Location.people). \
            filter(Person.id_status == 3). \
            group_by(Location.country). \
            order_by(db.func.count(Person.id).desc()). \
            all()
    else:
        deathQuantityByCountry = db.session.query(Location.country, db.func.count(Person.id)). \
            join(Location.people). \
            filter(Person.id_status == 3). \
            group_by(Location.country). \
            order_by(db.func.count(Person.id).asc()). \
            all()
    return deathQuantityByCountry


def get_RecQty_by_country():
    # Получить количество выздоровевших пациентов в каждой стране
    recQuantityByCountry = db.session.query(Location.country, db.func.count(Person.id)). \
        join(Location.people). \
        filter(Person.id_status == 1). \
        group_by(Location.country). \
        all()
    return recQuantityByCountry


def get_RecQty_by_country_ordered(sort_type):
    # Получить количество выздоровевших пациентов в каждой стране (сортированный)
    if sort_type == 'desc2':
        recQuantityByCountry = db.session.query(Location.country, db.func.count(Person.id)). \
            join(Location.people). \
            filter(Person.id_status == 1). \
            group_by(Location.country). \
            order_by(db.func.count(Person.id).desc()). \
            all()
    else:
        recQuantityByCountry = db.session.query(Location.country, db.func.count(Person.id)). \
            join(Location.people). \
            filter(Person.id_status == 1). \
            group_by(Location.country). \
            order_by(db.func.count(Person.id).asc()). \
            all()
    return recQuantityByCountry


def get_avg_DeathAge_by_country():
    # Получить средний возраст смерти для всех стран
    avgAgeByCountry = db.session.query(Location.country, db.func.avg(Person.age)). \
        join(Location.people). \
        filter(Person.id_status == 3). \
        group_by(Location.country). \
        all()
    return avgAgeByCountry

def get_avg_DeathAge_by_country_ordered(sort_type):
    #Получить средний возраст смерти для всех стран (сортированный)
    if sort_type == 'desc3':
        avgAgeByCountry = db.session.query(Location.country, db.func.avg(Person.age)). \
            join(Location.people). \
            filter(Person.id_status == 3). \
            group_by(Location.country). \
            order_by(db.func.avg(Person.age).desc()). \
            all()
    else:
        avgAgeByCountry = db.session.query(Location.country, db.func.avg(Person.age)). \
            join(Location.people). \
            filter(Person.id_status == 3). \
            group_by(Location.country). \
            order_by(db.func.avg(Person.age).asc()). \
            all()
    return avgAgeByCountry


def get_5top_symptom():
    #Получить 5 самых распространенных симптомов
    topSymptom = db.session.query(Symptom.name). \
        join(Person.symptoms). \
        group_by(Symptom.name). \
        order_by(db.func.count(Person.id).desc()). \
        all()
    return topSymptom


def get_max_exp_start():
    #Получить дату, когда госпитализировали наибольшее число людей

    maxExpDate = db.session.query(Person.exposure_start). \
        filter(Person.exposure_start != 'NA'). \
        group_by(Person.exposure_start). \
        order_by(db.func.count(Person.id).desc()). \
        all()
    return maxExpDate[0]


def get_death_symptom():
    #Получить симптом, который чаще всего наблюдался у пациентов с летальным исходом
    deathSymptom = db.session.query(Symptom.name). \
        filter(Person.id_status == 3). \
        join(Person.symptoms). \
        group_by(Symptom.name). \
        order_by(db.func.count(Person.id).desc()). \
        first()
    return deathSymptom[0]
