from flask import Flask,send_file, jsonify , request , make_response , send_from_directory, url_for
from flask_cors import cross_origin
from flask_jwt_extended import JWTManager,jwt_required
from datetime import timedelta



# create app
app = Flask(__name__)

# create jwt instance
jwt = JWTManager(app)

# add jwt secret key
app.config["JWT_SECRET_KEY"] = "api-laafigram" 

# add jwt access expired date
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)

# configuration de la base de donnee
app.config.from_object('config')

# secret_key for app
app.secret_key = "laafigram_app_key"


# put max size of file
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

#importer les controllers
from news.controllers  import ArticleController , CountryController,MediaController,TypeMediaController
from news.errors import *

# route principale
@app.route('/')
@cross_origin()
def index():
   return make_response(jsonify(message = 'Bienvenue sur notre api de produit')),200

@app.route('/news/api/v1/articles', methods=['GET', 'POST'])
@cross_origin()
def articles():
     if request.method == 'GET':
        return ArticleController().index()

     elif request.method == 'POST':
        return ArticleController().store(request)


@app.route('/news/api/v1/articles/<int:article_id> ', methods=['GET', 'PUT','DELETE'])
@cross_origin()
def handle_article(article_id):
    if request.method == 'GET':
       return ArticleController().show(article_id)

    elif request.method == 'PUT':
       return ArticleController().update(article_id, request)
   
    elif request.method == 'DELETE':
        return ArticleController().delete(article_id)


@app.route('/news/api/v1/countries', methods=['GET', 'POST'])
@cross_origin()
def countries():
     if request.method == 'GET':
        return CountryController().index()

     elif request.method == 'POST':
        return CountryController().store(request)


@app.route('/news/api/v1/countries/<int:country_id> ', methods=['GET', 'PUT','DELETE'])
@cross_origin()
def handle_country(country_id):
    if request.method == 'GET':
       return CountryController().show(country_id)

    elif request.method == 'PUT':
       return CountryController().update(country_id, request)
   
    elif request.method == 'DELETE':
        return CountryController().delete(country_id)


@app.route('/news/api/v1/media', methods=['GET', 'POST'])
@cross_origin()
def media():
     if request.method == 'GET':
        return MediaController().index()

     elif request.method == 'POST':
        return MediaController().store(request)


@app.route('/news/api/v1/media/<int:media_id> ', methods=['GET', 'PUT','DELETE'])
@cross_origin()
def handle_media(media_id):
    if request.method == 'GET':
       return MediaController().show(media_id)

    elif request.method == 'PUT':
       return MediaController().update(media_id, request)
   
    elif request.method == 'DELETE':
        return MediaController().delete(media_id)




@app.route('/news/api/v1/typeMedia', methods=['GET', 'POST'])
@cross_origin()
def type_media():
     if request.method == 'GET':
        return TypeMediaController().index()

     elif request.method == 'POST':
        return TypeMediaController().store(request)


@app.route('/news/api/v1/media/<int:type_media_id> ', methods=['GET', 'PUT','DELETE'])
@cross_origin()
def handle_type_media(type_media_id):
    if request.method == 'GET':
       return TypeMediaController().show(type_media_id)

    elif request.method == 'PUT':
       return TypeMediaController().update(type_media_id, request)
   
    elif request.method == 'DELETE':
        return TypeMediaController().delete(type_media_id)



