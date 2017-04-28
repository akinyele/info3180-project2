from . import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80), unique=True)
    gender = db.Column(db.String(80))
    age = db.Column(db.String(20))
    image = db.Column(db.String(80))
    token = db.Column(db.String(80),unique=True)
    # wishlist = db.Column(db.Text)
    
    
    
    def __init__(self, email, name, password, gender, age, image, token):
        self.email = email
        self.name = name
        self.password = password
        self.gender = gender
        self.age = age
        self.image = image
        self.token = token
        # self.wishlist = wishlist
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.name)
        
        
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    userid = db.Column(db.String(80))
    title = db.Column(db.String(80))
    description = db.Column(db.String(80))
    url = db.Column(db.Text)
    thumbnail_url = db.Column(db.Text)
    
    
    def __init__(self, userid,title,description,url, thumbnail_url):
        self.userid = userid
        self.title= title
        self.description=description
        self.url = url
        self.thumbnail_url = thumbnail_url
        
    
    def __repr__(self):
        return '<User %s> <Title %s> <Description %s> <URL %s> <Thumbnail_URL %s>' % (self.name, self.title, self.description,self.url, self.thumbnail_url)
           
    
    
    
