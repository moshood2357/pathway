class GeneralConfig:
    ADMIN_EMAIL='admin@foodcircle.com'

class TestConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/path_db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class LiveConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/path_db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False 