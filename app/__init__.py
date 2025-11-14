from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from config import config  
import os

from dotenv import load_dotenv
load_dotenv()

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name: str = os.environ.get("production", "default")) -> Flask:
    """
    Створення екземпляру додатку Flask.
    """
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from .users import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from .products import products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from .views import main_bp
    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    return app