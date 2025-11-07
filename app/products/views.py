from . import products_bp 
from flask import render_template

@products_bp.route('/') 
def all_products():
    products_list = ["Ноутбук", "Мишка", "Клавіатура"]
    
    return render_template("products/products.html", products=products_list)

@products_bp.route('/<int:product_id>')
def product_details(product_id):
    return f"<h1>Деталі для продукту {product_id}</h1>"