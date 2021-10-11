# import SQLAlchemy
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from news.views import app
from werkzeug.security import generate_password_hash
from datetime import date, datetime

# create database connexion
db = SQLAlchemy(app)

#create user classe
class User(db.Model):

    """Model for user accounts."""
    __tablename__ = 'users'

    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False ,unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)   

    def __repr__(self):
        return '<User {}>'.format(self.id)
    
     #json object 
    def json(self):
        return {
             "id":self.id,
             "username":self.username,
             "email":self.email,
             "create_at": format_datetime(self.created_at), 
             "update_at": format_datetime(self.updated_at)
             }

#create classe
class Country(db.Model):

    """Model for country."""

    #rename table
    __tablename__ = 'countries'

    #create field
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)   
    
    # relationship with product table
    articles = db.relationship('Article', backref='country')
    
    def __repr__(self):
        return '<Country {} {}>'.format(self.id, self.country_name)

    #json object 
    def json(self):
        return { 
            "id":self.id,
            "country_name":self.country_name,
            "create_at": format_datetime(self.created_at), 
             "update_at": format_datetime(self.updated_at) 
            }

class Article(db.Model):

    """Model for articles."""

    #rename table
    __tablename__ = 'articles'

    #create field
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_published = db.Column(db.String(80), nullable=False)
    source = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)   
    
    # ajout de la cle etranger 
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    
    # formatte l'affichage
    def __repr__(self):
        return '<Article {} {} {} {} {}>'.format(self.id, self.title, self.content , self.date_published, self.source )

    #json object 
    def json(self):
        return { 
            "id":self.id,
            "title":self.title, 
            "content":self.content, 
            "date_published":self.date_published, 
            "source":self.source, 
             "country" : Country.query.get(self.country_id).country_name,
            "create_at": format_datetime(self.created_at), 
             "update_at": format_datetime(self.updated_at)
            }

class Media(db.Model):

    """Model for medias."""
    
    #rename table
    __tablename__ = 'medias'

    #create field
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)   
    
    # ajout de la cle etranger 
    type_media_id = db.Column(db.Integer, db.ForeignKey('type_medias.id'))
    
    # formatte l'affichage
    def __repr__(self):
        return '<Media {} {} {}>'.format(self.id, self.url)

    #json object 
    def json(self):
        return { 
            "id":self.id,
            "url":self.url ,
            "create_at": format_datetime(self.created_at), 
             "update_at": format_datetime(self.updated_at)
            }

#create classe
class TypeMedia(db.Model):

    """Model for type_medias."""

    #rename table
    __tablename__ = 'type_medias'

    #create field
    id = db.Column(db.Integer, primary_key=True)
    type_medias_name = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)   
    
    # relationship with product table
    medias = db.relationship('Media', backref='media')

    # formatte l'affichage
    def __repr__(self):
        return '<TypeMedia {} {} {}>'.format(self.id, self.type_medias_name)

    #json object 
    def json(self):
        return { 
            "id":self.id,
            "type_media_name":self.type_medias_name,
            "create_at": format_datetime(self.created_at), 
             "update_at": format_datetime(self.updated_at) 
            }

def create_default_user():
    new_user = User(username="luc ouedraogo", email="luc@gmail.com", password=generate_password_hash("admin"))
    # ajouter en base 
    db.session.add(new_user)
    db.session.commit()

def format_datetime(date):
    return date.strftime("%d/%m/%Y")
