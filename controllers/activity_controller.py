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

            # Check object format
            object_params = self.valid_object_format(request)
            if object_params == False:
                content = {
                    "error": True,
                    "message": "Wrong object format"
                }
                return content, 400

            # Check object is exists
            post_verb_table_mapping = {
                'post': 'posts',
                'photo': 'photos'
            }
            post_object = db.table(post_verb_table_mapping[object_params['object_type']]).where({
                'id': object_params['object_id']
            }).first()

            if post_object is None:
                content = {
                    "error": True,
                    "message": "Object is not found"
                }
                return content, 400

            # Get target
            target = db.table('users').where({
                'id': post_object['user_id']
            }).first()

            # Write to activity table
            activity_params = self.merge_two_dicts(params, object_params)
            activity_params['target_id'] = target['id']
            activity_params['target_name'] = target['name']
            db.table('activities').insert(activity_params)

            content = {
                "verb": verb,
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
