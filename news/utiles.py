from flask import request,Request, make_response, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
#from news.models import Participant, Room , Meet
from sys import exc_info
from traceback import format_exception

def check_hour(hour):
    # split hour
    test= [ int(h) for h in hour.split(':')]
    hour , minutes = test[0], test[1]
    if (hour >= 0 and hour <=23) and ( minutes >= 0 and minutes <=59):
        return True
    else:
        return False

def get_current_date():
    return datetime.utcnow()

def check_json_data(data):

    if data == None:
        return 0
    elif data == '':
        return 1 
    else:
        return False

def check_validity_data(data, entity):

    if entity == 'article':
        if  not 'title' in data: 
           return 'title required'

        elif not 'content' in data:
            return 'content required'

        elif not 'date_published'  in data:
            return 'date_published required'  

        elif not 'source' in data:
            return 'source required'

        elif not 'country' in data:
             return 'country required'
    
    elif entity == 'country':
        if  not 'country_name' in data: 
           return 'country_name required'
        
    elif entity == 'media':
        if not 'url' in data:
            return 'url required'

    elif entity == 'type_media':
        if not 'type_medias_name' in data:
            return 'type_medias_name required'
      
    return ''

def remove(string):
    return "".join(string.split())

def print_exception():
    etype, value, tb = exc_info()
    info, error = format_exception(etype, value, tb)[-2:]
    print(f'Exception in:\n{info}\n{error}')

def check_request_json(request: Request):
    if not request.json:
        return make_response(jsonify(status='failed', response='Json object required')),400

