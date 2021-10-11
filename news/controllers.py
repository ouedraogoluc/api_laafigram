from flask import make_response, jsonify, Request
from news.models import Country, User , db,Article,TypeMedia,Media
from news.utiles import *
import json, os
from news.views import app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import string


class ArticleController:

    def index(self):
        try:
            query =   Article.query.order_by(Article.created_at.desc())
            results = [Article.json(article) for article in query ]
            return make_response(jsonify(articles= results, total=len(results))),200
        except SQLAlchemyError as e:
            print(str(e))
            
            return make_response(jsonify(response= 'Error Server '  )),500

    def store(self, request: Request):
        try:
            check_request_json(request=request)
            data = request.json
            message = check_validity_data(data=data, entity='article')
            if message == '':
                country=Country.query.filter(Country.country_name == data["country"]).first()
                print(country)
                
                if country:
                    new_article=Article(title=data["title"], content=data["content"], date_published=data["date_published"], source=data["source"], country=country )
                    db.session.add(new_article) 
                    db.session.commit()
                else:
                    return make_response(jsonify(message= 'country not found ' )),404
  
                return make_response(jsonify(message= 'Article successfully created ' )),201
            else:
                return make_response(jsonify(message=message )),400

        except (SQLAlchemyError , Exception) as e:
            db.session.rollback()
            print(type(e), e)
            print_exception()
            return make_response(jsonify(response= 'Error Server ' )),500
        
    def show(self, id):
        try:
            article = Article.query.filter(Article.id == id).first()
            if article:
                return make_response(jsonify(status='success', article=article.json(article))),200
            else:
                return make_response(jsonify(status='failed', response='Not found ressource')),404
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(response= 'Error Server '  + print_exception()  )),500

    def update(self, id, request):
        pass

    def delete(self, id):
        try:
            delete_article =    Article.query.get(id)
            if delete_article:
                db.session.delete(delete_article)
                db.session.commit()
                return make_response(jsonify(status='success', response='article successfully delete')),200
            else:
                return make_response(jsonify(status='failed', response='article not exists')),404
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(error='Error server')),500


class CountryController:

    def index(self):
        try:
            query =   Country.query.order_by(Country.created_at.desc())
            results = [Country.json(country) for country in query ]
            return make_response(jsonify(countries= results, total=len(results))),200
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(response= 'Error Server '  )),500

    def store(self, request: Request):
        try:
            check_request_json(request=request)
            data = request.json
            message = check_validity_data(data=data, entity='country')
            if message == '':
                country=Country.query.filter(Country.country_name == data["country_name"]).first()
                if country is None:
                    new_country = Country(country_name=data['country_name'])
                    db.session.add(new_country) 
                    db.session.commit()
                else:
                    return make_response(jsonify(message= 'country already exists found ' )),202
  
                return make_response(jsonify(message= 'country  successfully created ' )),201
            else:
                return make_response(jsonify(message=message )),400

        except (SQLAlchemyError , Exception) as e:
            db.session.rollback()
            print(type(e), e)
            return make_response(jsonify(response= 'Error Server ' )),500
        
    def show(self, id):
        try:
            article = Article.query.filter(Article.id == id).first()
            if article:
                return make_response(jsonify(status='success', article=article.json(article))),200
            else:
                return make_response(jsonify(status='failed', response='Not found ressource')),404
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(response= 'Error Server '  + print_exception()  )),500

    def update(self, id, request):
        pass

    def delete(self, id):
        try:
            delete_article =    Article.query.get(id)
            if delete_article:
                db.session.delete(delete_article)
                db.session.commit()
                return make_response(jsonify(status='success', response='article successfully delete')),200
            else:
                return make_response(jsonify(status='failed', response='article not exists')),404
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(error='Error server')),500


class MediaController:

    def index(self):
        try:
            query =   Media.query.order_by(Media.created_at.desc())
            results = [Media.json(media) for media in query ]
            return make_response(jsonify(medias= results, total=len(results))),200
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(response= 'Error Server '  )),500

    def store(self, request: Request):
        try:
            check_request_json(request=request)
            data = request.json
            message = check_validity_data(data=data, entity='media')
            if message == '':
                media=Media.query.filter(Media.url == data["url"]).first()
                if media is None:
                    new_media = Media(url=data['url'])
                    db.session.add(new_media) 
                    db.session.commit()
                else:
                    return make_response(jsonify(message= 'media already exists found ' )),202
  
                return make_response(jsonify(message= 'media  successfully created ' )),201
            else:
                return make_response(jsonify(message=message )),400

        except (SQLAlchemyError , Exception) as e:
            db.session.rollback()
            print(type(e), e)
            return make_response(jsonify(response= 'Error Server ' )),500
        
    def show(self, id):
        try:
            media = Media.query.filter(Media.id == id).first()
            if media:
                return make_response(jsonify(status='success', media=media.json(media))),200
            else:
                return make_response(jsonify(status='failed', response='Not found ressource')),404
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(response= 'Error Server '  + print_exception()  )),500

    def update(self, id, request):
        pass

    def delete(self, id):
        try:
            delete_media =Media.query.get(id)
            if delete_media:
                db.session.delete(delete_media)
                db.session.commit()
                return make_response(jsonify(status='success', response='media successfully delete')),200
            else:
                return make_response(jsonify(status='failed', response='media not exists')),404
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(error='Error server')),500


class TypeMediaController:

    def index(self):
        try:
            query =   TypeMedia.query.order_by(TypeMedia.created_at.desc())
            results = [TypeMedia.json(typemedia) for typemedia in query ]
            return make_response(jsonify(typemedias= results, total=len(results))),200
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(response= 'Error Server '  )),500

    def store(self, request: Request):
        try:
            check_request_json(request=request)
            data = request.json
            message = check_validity_data(data=data, entity='type_media')
            if message == '':
                typemedia=TypeMedia.query.filter(TypeMedia.type_medias_name == data["type_medias_name"]).first()
                if typemedia is None:
                    new_type_media = TypeMedia(type_medias_name=data['type_medias_name'])
                    db.session.add(new_type_media) 
                    db.session.commit()
                else:
                    return make_response(jsonify(message= 'media already exists found ' )),202
  
                return make_response(jsonify(message= 'media  successfully created ' )),201
            else:
                return make_response(jsonify(message=message )),400

        except (SQLAlchemyError , Exception) as e:
            db.session.rollback()
            print(type(e), e)
            return make_response(jsonify(response= 'Error Server ' )),500
        
    def show(self, id):
        try:
            media = TypeMedia.query.filter(TypeMedia.id == id).first()
            if media:
                return make_response(jsonify(status='success', media=media.json(media))),200
            else:
                return make_response(jsonify(status='failed', response='Not found ressource')),404
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(response= 'Error Server '  + print_exception()  )),500

    def update(self, id, request):
        pass

    def delete(self, id):
        try:
            delete_media =TypeMedia.query.get(id)
            if delete_media:
                db.session.delete(delete_media)
                db.session.commit()
                return make_response(jsonify(status='success', response='media successfully delete')),200
            else:
                return make_response(jsonify(status='failed', response='media not exists')),404
        except SQLAlchemyError as e:
            print(str(e))
            return make_response(jsonify(error='Error server')),500

