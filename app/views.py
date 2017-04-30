"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify, g
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from models import UserProfile, Wishlist
import hashlib, thumbnail_scrapper, logging
from functools import wraps
from sqlalchemy import exc




############
###
### API routes and Methods
###
############


# Create a Basic @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'basic':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Basic'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Basic + \s + token'}), 401


    token = parts[1]
    g.token = token
    
    
    try:
        g.cur_id = UserProfile.query.filter_by(token=token).first().id
    except AttributeError: 
        g.cur_id = ""
    except exc.SQLAlchemyError:
        return jsonify( error = True, data = {} , message =  "SERVER ERROR Database unreachable"), 501
    
   
    return f(*args, **kwargs)

  return decorated
  

def verify_user(userid, cur_id):
    """ User to verify the current user obtained by the request token with the proveided user """ 
    if userid != str(cur_id):
        return False
    return True


@app.route('/api/users/register', methods=["POST"])
@requires_auth
def API_register():
    
    token = g.token
    
    
    email = request.json["email"]
    name = request.json["name"]
    password = request.json["password"]
    age = request.json["age"]
    gender = request.json["gender"]
    image = request.json["image"]
    
    # logging.info("data recieved " + image + " gender " + gender)
    
    User = UserProfile(email, name, password, age, gender,image,token)
    try:
        db.session.add(User)
        db.session.commit()
    except exc.SQLAlchemyError:
        return jsonify( error = True, data = {} , message =  "SERVER ERROR Database unreachable"), 501
    
        
    
    data = { 'user' : {
        
                "email": User.email,
                "name": User.name,
                "password": User.password,
                "age": User.age,
                "gender": User.gender,
                "image": User.image 
        
            }
        }
        
    return jsonify( error = None, data = data , message =  "success"), 201
    

@app.route('/api/users/login',methods=['POST'])
@requires_auth
def API_login():
    #Login a User [POST]
    # If there is an error then set the `error` property to `true` and leave the `data` property
    # as an empty object. Also ensure that the `message` property is set with the appropriate error
    # message.
    
    token = g.token
    
    email = request.json['email']
    
    try:
        user = UserProfile.query.filter_by(token = token).first()
    except exc.SQLAlchemyError:
        return jsonify( error = True, data = {} , message =  "SERVER ERROR Database unreachable"), 500
    
    
    if not user :
        return jsonify(error= True, message = "incorrect username or password", data = {} )
        
    
    data = {
        'user' : {
            "email" : user.email,
            "name" : user.name,
            ## I NEED THIS INFO WHEN THE USER LOGS IN 
            "age": user.age,
            "gender": user.gender,
            "image": user.image,
            "id":user.id
        }
    }
    
    
    return jsonify(error = None, message = "Sucess", data = data)


@app.route('/api/users/<userid>/wishlist', methods= ["POST"])
@requires_auth
def add_item(userid):
    # """
    # Create a New Wishlist Item [POST]
    # You may create new wishlist items using this action. It takes a JSON
    # object containing a userid, title, description, product url and thumbnail url.
    # """
    
    # if not verify_user(userid,g.cur_id): 
    #     return jsonify(error = True, message = "Unauthorized Access incorrect user token" + str(g.cur_id)+"vs"+ str(userid) , data={}), 404
    
    
    title = request.json['title']
    description = request.json['description']
    url=request.json['url']
    thumbnail_url=request.json['thumbnail_url']
    
    wishlistItem = Wishlist(str(userid), title, description, url, thumbnail_url)
    db.session.add(wishlistItem)
    db.session.commit()
    
    data = {
        "item" : {
            "id":  wishlistItem.id,
            "title": wishlistItem.title,
            "description": wishlistItem.description,
            "url": wishlistItem.url,
            "thumbnail_url": wishlistItem.thumbnail_url
        }
    }
    
    return jsonify(message="success", error=None, data= data)



@app.route('/api/users/<userid>/wishlist', methods= ["GET"])
@requires_auth
def get_wishlist(userid):
    # List All Items in a Users Wishlist [GET]
    # Get all the items in a specific users' wishlist.
    
    # If there is an error then set the `error` property to `true` and leave the `data` property
    # as an empty object. Also ensure that the `message` property is set with the appropriate error
    # message.
    
    # if not verify_user(userid, g.cur_id): 
    #     return jsonify(error = True, message = "Unauthorized Access incorrect user token for userid : "+ str(g.cur_id), data={}), 400
    
    
    
    # results = Wishlist.query.filter_by(userid=str(userid)).all()
    
    
    results = Wishlist.query.filter_by(userid=userid).all()
    
    
    if len(results)<1:
        return jsonify(error=True, message = str(len(results))+" Item currenly in wishlist", data={})
    
    items = []
    for result in results:
        items.append({
            "id":result.id,
            "title":result.title,
            "url":result.url,
            "thumbnail_url":result.thumbnail_url
        }) 
    
    data = { "items":items }
    
    
    return jsonify(error=None, message= "success", data=data)


@app.route('/api/thumbnails', methods=["GET","POST"])
@requires_auth
def thumbnails():
    # Get thumbnail images from a URL [GET]
    # Take a url and scrape the page for any images and return the URL for each image found.
    
    # If there is an error then set the `error` property to `true` and leave the `data` property
    # as an empty object. Also ensure that the `message` property is set with the appropriate error
    # message.
    
    #url = request.json["url"]
    
    blob = request.get_json(force=True)
    
    thumbnails=[]
    
    
    thumbnails=thumbnail_scrapper.getImages(blob['url'])
    
    
    if not thumbnails:
        return jsonify(message="Unable to extract thumbnails from "+url, error=True, data={})
        
    data = {
        "thumbnails":thumbnails
    }
    
    
    return jsonify(message="Success", error=None, data=data)



@app.route('/api/users/<userid>/wishlist/<itemid>', methods=["DELETE"])
@requires_auth
def delete(userid,itemid):
    # Delete items from a Users Wishlist [DELETE]
    
    
    itemid = request.json['id']
    
    item = Wishlist.query.filter_by(id=itemid).first()
    
    db.session.delete(item)
    db.session.commit()
    
    
    return  jsonify(data={}, message="success", error=None)








#####################
####
####    Front End Routes and Methods
####
###################

# class wishlistUser(object):
    
#     def __init__(self, email, username):
#         self.email = email
#         self.username = username
        
#     def get_id(self):
#         try:
#             return unicode(self.email)  # python 2 support
#         except NameError:
#             return str(self.email)  # python 3 support

        
    
    
    



@app.route("/token", methods=["POST"])
def genToken():
    """ A request is made to the this url so a token can be generated to be sent to the API """
    
    password = request.json["password"]
    email = request.json["email"]
    
    token = hashlib.md5(password+email).hexdigest()
    return token
    
    


@app.route('/')

def home():
    """Render website's home page."""
    render_template('home.html')
    return render_template('home.html')




@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('home.html')

@app.route('/wishlist')
def wihslist():
    """Render the website's about page."""
    return render_template('home.html')
    
@app.route('/addwish')
def addwish():
    """Render the website's about page."""
    return render_template('home.html')
    
    




@app.route("/login")
def login():
    return render_template("home.html")
    
    
    

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
# @login_manager.user_loader
# def load_user(email):
#     return wishlistUser.get(self.email)



###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response



@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.errorhandler(501)
def server_error(error):
    """Custom 404 page."""
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
