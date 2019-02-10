import json
from config.bootstrap import app, db
from decorators.headers import valid_token, valid_json
from flask import g, request
from IPython import embed
from controllers import base_controller

class controller(base_controller.controller):

    @valid_token
    @valid_json
    def post(self):
        try:
            activity_params = {
                'time': 'now()'
            }

            token = request.headers['X-App-Key']
            current_user = db.table('users').where('auth_token', token).first()
            activity_params['actor_id'] = current_user['id']
            activity_params['actor_name'] = current_user['name']

            # Valid type : post, photo, comments, image, etc..
            valid_type = ['post', 'photo']
            try:
                if request.json['type'] not in valid_type:
                    raise Exception
            except Exception as e:
                content = {
                    "error": True,
                    "message": "Type is missing or not valid"
                }
                return content, 400

            # Must have content
            try:
                post_content = request.json['content']
            except Exception as e:
                content = {
                    "error": True,
                    "message": "Content is missing"
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

            post_object_id = db.table(post_verb_table_mapping[request.json['type']]).insert_get_id({
                'user_id': current_user['id'],
                'content': request.json['content'],
                'created_at': 'now()',
                'updated_at': 'now()'
            })

            activity_params['verb'] = 'post'
            activity_params['object_id'] = post_object_id
            activity_params['object_type'] = request.json['type']
            db.table('activities').insert(activity_params)

            content = {
                "type": request.json['type'],
                "object_id": post_object_id,
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
