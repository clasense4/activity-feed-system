import json
from config.bootstrap import app, db
from decorators.headers import valid_token, valid_json
from flask import g, request
from IPython import embed
from controllers import base_controller

class controller(base_controller.controller):

    @valid_token
    @valid_json
    def activity(self):
        try:
            params = {
                'time': 'now()'
            }

            # No need extra validation, handled by @valid_token
            # "actor":"ivan"
            token = request.headers['X-App-Key']
            current_user = db.table('users').where('auth_token', token).first()
            params['actor_id'] = current_user['id']
            params['actor_name'] = current_user['name']

            # Validate verb (like, post, share)
            #   "verb":"like"
            valid_verb = ['like', 'share']
            verb = request.json['verb']
            if str.lower(verb) in valid_verb:
                params['verb'] = verb
            else:
                content = {
                    "error": True,
                    "message": "Wrong verb format"
                }
                return content, 400

            # Validation for like
            if verb in ['like', 'share']:
                # Must have object and make sure it is valid
                # Must have target
                pass

        except Exception as e:
            app.logger.error(e)
            content = {
                "error": True,
                "message": "Something wrong on our side, sorry"
            }
            return content, 500
