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
            valid_verb = ['like', 'post', 'share', 'follow']
            verb = request.json['verb']
            if str.lower(verb) in valid_verb:
                params['verb'] = verb
            else:
                content = {
                    "error": True,
                    "message": "Wrong verb format"
                }
                return content, 400

            # Validation for post
            if verb == 'post':
                # Must have object
                object_params = self.valid_object_format(request)
                if object_params == False:
                    content = {
                        "error": True,
                        "message": "Wrong object format"
                    }
                    return content, 400

                # Create record in post/photo table
                """
                TODO : Add 'content' in verb 'post' including its validation
                post => Raw Text
                photo => Image URL
                """
                post_verb_table_mapping = {
                    'post': 'posts',
                    'photo': 'photos'
                }
                object_name = request.json['object'].split(":")[0]
                db.table(post_verb_table_mapping[object_name]).insert({
                    'user_id': params['actor_id'],
                    'content': "Foobar",
                    'created_at': 'now()',
                    'updated_at': 'now()'
                })

                activity_params = self.merge_two_dicts(params, object_params)
                db.table('activities').insert(activity_params)

                content = {
                    "verb": verb,
                    "message": "Activity recorded"
                }
                return content, 200

            if verb == 'follow':
                # Must have target
                target_params = self.valid_target(request)
                if target_params == False:
                    content = {
                        "error": True,
                        "message": "Target is not found"
                    }
                    return content, 400

                activity_params = self.merge_two_dicts(params, target_params)
                db.table('activities').insert(activity_params)

                content = {
                    "verb": verb,
                    "message": "Activity recorded"
                }
                return content, 200

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
