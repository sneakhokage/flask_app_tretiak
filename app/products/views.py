from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, request, jsonify
from .. import db
from .models import Product
from sqlalchemy import select 

@post_bp.route('/products', methods=['GET']) 
def get_products():
    stmt = select(Product).order_by(Product.name.desc()) 
    products = db.session.scalars(stmt).all()
    return render_template("products.html", products=products)
    
@post_bp.route('/products/<int:id>') 
def detail_post(id):
    product = db.session.get(Product, id)
    if not product:
        abort(404, description="Product not found") 
    return render_template("detail_post.html", 
                           product=product)