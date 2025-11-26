from flask import render_template, request, redirect, session
import math
import dao
from saleapp import app, login, admin, db
from saleapp.decorators import anonymous_required
from flask_login import login_user, current_user, logout_user, login_required
import cloudinary.uploader

@app.route("/")
def index():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    page = request.args.get("page")
    prods = dao.load_products(q=q, cate_id=cate_id, page=page)
    pages = math.ceil(dao.count_product()/app.config["PAGE_SIZE"])
    return render_template("index.html", prods=prods, pages=pages)

@app.route("/products/<int:id>")
def details(id):
    prod = dao.get_product_by_id(id)
    return render_template("product-details.html", prod=prod)

@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories()
    }

@app.route("/login", methods=["get", "post"])
@anonymous_required
def login_my_user():
    err_msg = None
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            return redirect("/")
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template("login.html", err_msg=err_msg)

@app.route("/login-admin", methods=["post"])
def login_admin_process():
    username = request.form.get("username")
    password = request.form.get("password")

    user = dao.auth_user(username, password)

    if user:
        login_user(user)
        return redirect("/admin")
    else:
        err_msg = "Tài khoản hoặc mật khẩu không đúng!"

@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = None
    if request.method.__eq__("POST"):
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password.__eq__(confirm):
            name = request.form.get('name')
            username = request.form.get("username")
            avatar = request.files.get('avatar')
            file_path = None

            if avatar:
                res = cloudinary.uploader.upload(avatar)
                file_path = res['secure_url']

            try:
                dao.add_user(name, username, password, avatar=file_path)
                return redirect('/login')
            except:
                db.session.rollback()
                err_msg = "Hệ thống đang bị lỗi! Vui lòng quay lại sau!"
        else:
            err_msg = "Mật khẩu không khớp!"

    return render_template("register.html", err_msg=err_msg)

@app.route('/cart')
def cart():
    session['cart'] = {
        "1": {
            "id": 1,
            "name": "Iphone 15 Promax",
            "price": 10000,
            "quantity": 2
        },
        "2": {
            "id": 2,
            "name": "Samsung Galaxy",
            "price": 9000,
            "quantity": 1
        }
    }
    return render_template('cart.html')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id=user_id)

if __name__=="__main__":
    app.run(debug=True)