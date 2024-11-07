from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import re
app = Flask(__name__)
# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(2), nullable=False)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/products/")
def products():
    products = Product.query.all()
    
    return render_template('products.html', products=products)

@app.route("/add-product/")
@app.route("/add-product/<product_name>/<price>")
def add_product(product_name = '', price = ''):
    if product_name and price:
        new_product = Product(product_name=product_name, price=price)
        db.session.add(new_product)
        db.session.commit()
    else:
        product_name = ''
        price = ''
        new_product = ''
    
    return render_template('add_product.html', product_name=product_name, price=price, new_product=new_product)

@app.route("/update-product/")
@app.route("/update-product/<id>/<price>")
def update_product(id = '', price = ''):
    if id and price:
        upd_product = Product.query.filter_by(id=id).first()
        upd_product.price = price
        db.session.commit()
    else:
        id = ''
        price = ''

    return render_template('update_product.html', upd_product=upd_product, id=id, price=price)

@app.route("/delete-product/")
@app.route("/delete-product/<id>/")
def delete_product(id = ''):
    if id:
        del_product = Product.query.filter_by(id=id).first()
        db.session.delete(del_product)
        db.session.commit()
    else:
        id = ''

    return render_template('delete_product.html', del_product=del_product, id=id)

