from flask import g, request, Response
from functools import wraps
from config.bootstrap import app, db
import json

def valid_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.has_key('X-App-Key'):
            token = request.headers['X-App-Key']
            user = db.table('users').where('auth_token', token).first()
            if (user == None):
                content = {
                    "error": True,
                    "message": "Key is not valid"
                }
                return content, 401
        else:
            content = {
                "error": True,
                "message": "Key is missing"
            }
            return content, 400
        return f(*args, **kwargs)
    return decorated_function

def valid_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if request.is_json == False:
                content = {
                    "error": True,
                    "message": "Must be json request"
                }
                return content, 400
            else:
                # Try if json can be decoded, it should return as dict
                request.get_json()
        except Exception as e:
            app.logger.error(e)
            content = {
                "error": True,
                "message": "Bad Request"
            }
            return content, 400

        return f(*args, **kwargs)
    return decorated_function