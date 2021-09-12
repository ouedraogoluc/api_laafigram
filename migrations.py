
from news.views import app

from news.models import db,create_default_user


with app.app_context():
    db.drop_all() #drop all tables
    db.create_all() # create all tables
    create_default_user()