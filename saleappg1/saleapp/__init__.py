from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "asjdahjsdaskdjahsd%#adsd"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/saledb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2
cloudinary.config(cloud_name='dy1unykph',
                  api_key='238791983534257',
                  api_secret='_J2MkfDJ1DwRe1uAn5TKozXup0U')

db = SQLAlchemy(app)

login = LoginManager(app)
