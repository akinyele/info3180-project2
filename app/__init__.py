from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_triangle import Triangle


app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://info3180:wishlist123@localhost/Wishlist_API"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://pzokgxmrhnihio:dc65deddbd1f4b0da50c8cf5e8384bcf0f46d11e2876168a4ce32308e358af03@ec2-54-225-119-223.compute-1.amazonaws.com:5432/d3fpge3uckt2o7"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

Triangle(app)
db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
