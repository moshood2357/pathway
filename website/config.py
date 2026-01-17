import os 


class GeneralConfig:
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@pathway.com')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(GeneralConfig):
#     # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/path_db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class LiveConfig(GeneralConfig):
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/path_db"
    DEBUG = False
    TESTING = False
    
    
