import os

# Secret key: local fallback, overridden by environment variable in production
SECRET_KEY = os.environ.get('SECRET_KEY', '979105ce4e5f8d0d244e4ab2f9043fee07153d0ecf7dabacbb295c3792e0c1d5')

# Database (local dev fallback)
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 
    'mysql+pymysql://root@localhost/path_db'
    
    # mysql+pymysql://root:password@localhost:3306/my_local_db
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Mail settings (development)
MAIL_SERVER = 'smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '73dee41d846e78')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '****c84e')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@pathway.com')
