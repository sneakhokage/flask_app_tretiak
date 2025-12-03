from flask import Blueprint

it_courses_bp = Blueprint('it_courses', __name__, template_folder='templates')

from . import views, models