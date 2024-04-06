class Config(object):
    DEBUG = True
    SECRET_KEY = 'some_key_123'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_DOMAIN = None  # Используйте домен по умолчанию
    SESSION_COOKIE_PATH = '/'
    SESSION_TYPE = 'filesystem'  # Можно выбрать другие типы хранения сессий
    POSTS_PER_PAGE = 1