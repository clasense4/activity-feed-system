import json
from config.bootstrap import app, db
from decorators.headers import valid_token, valid_json
from flask import g, request

class controller:

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
            valid_verb = ['like', 'post', 'share']
            verb = request.json['verb']
            if str.lower(verb) in valid_verb:
                params['verb'] = verb
            else:
                content = {
                    "error": True,
                    "message": "Wrong verb format"
                }
                return content, 400

            # Validate target user, can be null
            #   "target":"eric"
            target_name = request.json['target']
            target_user = db.table('users').where('name', target_name).first()
            if target_user:
                params['target_id'] = target_user['id']
                params['target_name'] = target_user['name']
            else:
                content = {
                    "error": True,
                    "message": "Target is not found"
                }
                return content, 400

            # Validate object, can be null
            #   "object":"photo:1",
            try:
                object_name = request.json['object'].split(":")[0]
                valid_object = ['post', 'photo']
                if object_name not in valid_object:
                    raise Exception

                # TODO : Support another type, uuid, integer
                object_id = int(request.json['object'].split(":")[1])

                # TODO : Check object is exists
                params['object_id'] = object_id
                params['object_type'] = object_name
            except Exception as e:
                content = {
                    "error": True,
                    "message": "Wrong object format"
                }
                return content, 400

            activities = db.table('activities').insert(params)

            content = {
                "message": "Activity recorded"
            }
            return content, 200

        except Exception as e:
            app.logger.error(e)
            content = {
                "error": True,
                "message": "Something wrong on our side, sorry"
            }
            return content, 500