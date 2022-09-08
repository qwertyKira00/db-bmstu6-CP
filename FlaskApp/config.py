class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://kira:password@localhost:5432/postgres"
    # Нужен для сессии, которая нужна при работе с мгновенными сообщениями
    # Используется для шифрования (автоматического) данных, перед тем как сохранить эти данные в браузере клиента
    SECRET_KEY = 'akscjvhv3asdfhn'
    SEND_FILE_MAX_AGE_DEFAULT = 0