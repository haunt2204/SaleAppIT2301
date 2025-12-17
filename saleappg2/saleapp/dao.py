import hashlib
import json

from sqlalchemy import func

from saleapp.models import Category, Product, User, Receipt, ReceiptDetail
from saleapp import app, db
from flask_login import current_user


def load_categories():
    # with open("data/category.json", encoding="utf-8") as f:
    #     return json.load(f)
    return Category.query.all()

def load_products(q=None, cate_id=None, page=None):
    # with open("data/product.json", encoding="utf-8") as f:
    #     products = json.load(f)
    #
    #     if q:
    #         products = [p for p in products if p["name"].find(q)>=0]
    #
    #     if cate_id:
    #         products = [p for p in products if p["cate_id"].__eq__(int(cate_id))]
    #
    #     return products
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))

    if cate_id:
        query = query.filter(Product.cate_id.__eq__(cate_id))

    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page)-1)*size
        end = start+size
        query = query.slice(start, end)

    return query.all()

def count_product():
    return Product.query.count()

def auth_user(username, password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()

def add_user(name,username,password,avatar):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    u = User(name=name,username=username.strip(),password=password.strip(),avatar=avatar)
    db.session.add(u)
    db.session.commit()

def count_product_by_cate():
    query = db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.cate_id.__eq__(Category.id), isouter=True).group_by(Category.id)

    print(query)

    return query.all()

def add_receipt(cart):
    r = Receipt(user=current_user)
    db.session.add(r)

    for p in cart.values():
        d = ReceiptDetail(prod_id=p['id'], receipt=r, unit_price=p['price'],quantity=p['quantity'])
        db.session.add(d)

    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_product_by_id(id):
    # with open("data/product.json", encoding="utf-8") as f:
    #     products = json.load(f)
    #
    #     for p in products:
    #         if p['id'].__eq__(id):
    #             return p
    #
    # return None
    return Product.query.get(id)

if __name__=="__main__":
    with app.app_context():
        print(count_product_by_cate())