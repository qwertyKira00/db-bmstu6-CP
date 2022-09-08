SIGNUP_EMAIL_FAIL = 6
SIGNUP_EMAIL_EMPTY_FAIL = 5
SIGNUP_EMAIL_SUCCESS = 0
SIGNUP_PASSWORD_LENGTH_FAIL = 4
SIGNUP_PASSWORD_CONTENT_FAIL = 3
SIGNUP_PASSWORD_SUCCESS = 0

SIGNIN_EMAIL_FAIL = 1
SIGNIN_EMAIL_SUCCESS = 0
SIGNIN_PASSWORD_FAIL = 2
SIGNIN_PASSWORD_SUCCESS = 0

PASSWORD_LENGTH = 8

NEW_USER_ADD_FAIL = 10
NEW_USER_ADD_SUCCESS = 0

NAME_EMPTY_FAIL = 7
NAME_SUCCESS = 0
LASTNAME_EMPTY_FAIL = 8
LASTNAME_SUCCESS = 0
DATE_INVALID = 9
DATE_SUCCESS = 0
ADDRESS_INVALID = 13
ADDRESS_SUCCESS = 0
PRIVATE_OFFICE_SUCCESS = 0

NEW_PRIVATE_OFFICE_ADD_FAIL = 11
NEW_PRIVATE_OFFICE_ADD_SUCCESS = 0

UPDATE_PRIVATE_OFFICE_ADD_FAIL = 14
UPDATE_PRIVATE_OFFICE_ADD_SUCCESS = 0

QUERY_NAME_FAIL = 14
QUERY_NAME_SUCCESS = 0
QUERY_DESCRIPTION_FAIL = 15
QUERY_DESCRIPTION_SUCCESS = 0
SQL_ERROR = 16
SQL_SUCCESS = 0
CREATE_QUERY_SUCCESS = 0

PSYCOPG2_ERROR = 17
PSYCOPG2_SUCCESS = 0

NEW_QUERY_ADD_FAIL = 17
NEW_QUERY_ADD_SUCCESS = 0

SERVER_EMAIL = 'covidmonitoringnoreply@gmail.com'
SUBJECT = 'Email address verification'
EMAIL_TEXT_PREV = 'To complete the setup of your COVIDMonitoring account, we need to make sure this is your email address.' \
             '\nUse this security code to verify your email address: '
EMAIL_TEXT_POST = '\n\nIf you have not registered for COVIDMonitoring, ignore this message.' \
    ' Someone may have entered your email address by mistake.'
EMAIL_TEXT_SIGNATURE = '\n\nSincerely,\ntechnical support service for COVIDMonitoring accounts.'
CODE = 4
CODE_FAIL = 12

ROLE_USER = 0
ROLE_ADMIN = 1

errors = {
    '1': 'Такая учетная запись CovidMonitoring не существует. Введите другую учетную запись или зарегистрируйте новую',
    '2': 'Пароль не верен. Введите корректный пароль',
    '3': 'Пароль должен содержать цифры, строчные символы, прописные символы',
    '4': 'Пароль должен содержать не менее 8 символов',
    '5': 'Введите корректный адрес электронной почты',
    '6': ' уже является учетной записью CovidMonitoring. Выберите другой адрес электронной почты',
    '7': 'Пожалуйста, введите корректное имя пользователя',
    '8': 'Пожалуйста, введите корректную фамилию пользователя',
    '9': 'Пожалуйста, введите корректную дату',
    '10': 'Пользователь не может быть зарегистрирован (ошбика сервера)',
    '11': 'Личный кабинет не может быть создан (ошибка сервера)',
    '12': 'Введенный код неверен',
    '13': 'Выберите улицу проживания из предложенного списка',
    '14': 'Пожалуйста, введите корректное название запроса',
    '15': 'Пожалуйста, введите корректный текст запроса',
    '16': 'SQl запрос неверен (ошибка при выполнении запроса)',
    '17': 'Запрос не может быть создан (ошбика сервера)'
}
