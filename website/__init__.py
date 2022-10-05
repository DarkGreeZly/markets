from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
DB_NAME = 'market_db.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sefnolewn lsnefoesl'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .pages import pages

    app.register_blueprint(pages, url_prefix='/')

    from .models import User, Market, Product

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'pages.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    admin = Admin(app, name='Market', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session, name='User'))
    admin.add_view(ModelView(Market, db.session, name='Market'))
    admin.add_view(ModelView(Product, db.session, name='Product'))
    return app

def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    else:
        print('Database exists!')

