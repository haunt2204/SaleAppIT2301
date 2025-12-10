import json
from datetime import datetime
from saleapp import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from enum import Enum as RoleEnum


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2

class Base(db.Model):
    __abstract__=True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name

class User(Base, UserMixin):
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    avatar = Column(String(300), default="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")
    role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref="user", lazy=True)

class Category(Base):
    products = relationship('Product', backref="category", lazy=True)

class Product(Base):
    price = Column(Float, default=0.0)
    image = Column(String(300), default="https://res.cloudinary.com/dy1unykph/image/upload/v1741254148/aa0aawermmvttshzvjhc.png")
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    description = Column(Text)
    details = relationship('ReceiptDetail', backref='product', lazy=True)

class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())

class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    prod_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    unit_price = Column(Float, default=0)
    quantity = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


if __name__=="__main__":
    with app.app_context():
        db.create_all()
        c1 = Category(name="Laptop")
        c2 = Category(name="Mobile")
        c3 = Category(name="Tablet")

        db.session.add_all([c1,c2,c3])

        with open("data/product.json", encoding="utf-8") as f:
            products = json.load(f)

            for p in products:
                prod = Product(**p)
                db.session.add(prod)

        db.session.commit()

        # print(c1)
        import hashlib

        u1 = User(name="User", username="user", password=hashlib.md5("123".encode("utf-8")).hexdigest())
        u2 = User(name="Admin", username="admin", password=hashlib.md5("123".encode("utf-8")).hexdigest(), role=UserRole.ADMIN)

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()