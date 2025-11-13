from flask import Blueprint

post_bp = Blueprint('product', __name__,template_folder="templates/products", static_folder="static")

from . import views
from . import models