import json
from config.bootstrap import app, db
from decorators.headers import valid_token, valid_json
from flask import g, request
from IPython import embed
from controllers import base_controller

class controller(base_controller.controller):

    @valid_token
    @valid_json
    def unfollow(self):
        try:
            activity_params = {
                'time': 'now()'
            }

            token = request.headers['X-App-Key']
            current_user = db.table('users').where('auth_token', token).first()

            # Check if user not found
            target_user = self.valid_user(request.json['unfollow'])
            if  target_user == False:
                content = {
                    "error": True,
                    "message": "User not found"
                }
                return content, 400

            # Check if trying to unfollow itself
            if target_user['id'] == current_user['id']:
                content = {
                    "error": True,
                    "message": "You can't unfollow yourself"
                }
                return content, 400

            # TODO : Update table users
            # TODO : Check for SQL injection
            db.table('users').where('id', current_user['id']).update({
                'follow_ids': db.raw('array_remove(follow_ids, '+str(int(target_user['id']))+')')
            })

            # TODO : Save activity
            activity_params['actor_id'] = current_user['id']
            activity_params['actor_name'] = current_user['name']
            activity_params['verb'] = 'unfollow'
            activity_params['target_id'] = target_user['id']
            activity_params['target_name'] = target_user['name']

            db.table('activities').insert(activity_params)

            content = {
                "verb": "unfollow",
                "message": "User unfollowed"
            }
            return content, 200
        except Exception as e:
            app.logger.error(e)
            content = {
                "error": True,
                "message": "Something wrong on our side, sorry"
            }
            return content, 500