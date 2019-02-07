import json
from config.bootstrap import app, db
from decorators.headers import valid_token, valid_json
from flask import g, request

class controller:

    @valid_token
    def me(self):
        try:
            token = request.headers['X-App-Key']
            current_user = db.table('users').where('auth_token', token).first()

            return dict(current_user), 200

        except Exception as e:
            app.logger.error(e)
            content = {
                "error": True,
                "message": "Something wrong on our side, sorry"
            }
            return content, 500
