import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-for-lab-4'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views

from .users import users_bp 
app.register_blueprint(users_bp, url_prefix='/users')

from .products import products_bp
app.register_blueprint(products_bp, url_prefix='/products')

from .posts import posts_bp
app.register_blueprint(posts_bp, url_prefix='/post')