from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail





db = SQLAlchemy()
mail = Mail()

def create_app():
    from website import config
    from website.models import db
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py',silent=True)
    app.config.from_object(config.LiveConfig)
    # instance_relative_config=True
    csrf = CSRFProtect(app)

    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    Migrate(app, db) 
    
    
    
    from website.views import views
    from website.auth import  auth
    from website.admin import admin


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    return app


app = create_app()
