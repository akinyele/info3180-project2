from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_triangle import Triangle


app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://info3180:wishlist123@localhost/Wishlist_API"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://argwfcrcooizrs:08f022a4819b7993f8c278d3b84dfc3e5613d715b6e5a074dc2d66d948ed6670@ec2-174-129-41-23.compute-1.amazonaws.com:5432/d85lpejkfivj6r"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

Triangle(app)
db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
