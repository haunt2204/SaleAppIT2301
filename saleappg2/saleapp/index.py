import math
from click import confirm
from flask import render_template, request, redirect, session, jsonify
import dao
from saleapp import app, login, admin, db
from flask_login import login_user, current_user, logout_user
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
    return render_template("product-details.html", prod=dao.get_product_by_id(id))


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect('/')

    err_msg = None

    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template("login.html", err_msg=err_msg)

@app.route('/admin-login', methods=['post'])
def admin_login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username, password)

    if user:
        login_user(user)
        return redirect('/admin')
    else:
        err_msg = "Tài khoản hoặc mật khẩu không đúng!"

@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories()
    }

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/register", methods=['get','post'])
def register():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password != confirm:
            err_msg = "Mật khẩu không khớp!"
        else:
            name = request.form.get('name')
            username = request.form.get('username')
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
    return render_template('register.html', err_msg=err_msg)

@app.route('/cart')
def cart():

    # session['cart'] = {
    #     "1": {
    #         "id": "1",
    #         "name": "Iphone 15 ProMax",
    #         "price": 1500,
    #         "quantity": 2
    #     },
    #     "2": {
    #         "id": "2",
    #         "name": "Samsung Galaxy",
    #         "price": 1000,
    #         "quantity": 1
    #     },
    # }

    return render_template('cart.html')

@app.route('/api/carts', methods=['post'])
def add_to_cart():
    cart = session.get('cart')

    if not cart:
        cart = {}

    id = str(request.json.get('id'))

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            'name': request.json.get('name'),
            'price': request.json.get('price'),
            'quantity': 1
        }

    session['cart'] = cart

    print(session['cart'])

    return jsonify({
        'total_quantity': 0,
        "total_amount": 0
    })


if __name__=="__main__":
    with app.app_context():
        app.run(debug=True)