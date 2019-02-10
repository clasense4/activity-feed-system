import json
from config.bootstrap import app, db
from decorators.headers import valid_token, valid_json
from flask import g, request
from IPython import embed
from controllers import base_controller

class controller(base_controller.controller):

    @valid_token
    def my(self):
        try:
            token = request.headers['X-App-Key']
            current_user = db.table('users').where('auth_token', token).first()

            my_feed = db.table('activities').select(
                'actor_name', 'verb', 'object_id', 'object_type', 'target_name', 'time'
            ).where({
                'actor_id': current_user['id']
            }).order_by('time', 'desc').get().to_json()

            content = {
                "my_feed": json.loads(my_feed),
                "next_url": ""
            }
            return content, 200
        except Exception as e:
            app.logger.error(e)
            content = {
                "error": True,
                "message": "Something wrong on our side, sorry"
            }
            return content, 500


    @valid_token
    def friends(self):
        try:
            token = request.headers['X-App-Key']
            current_user = db.table('users').where('auth_token', token).first()

            friends_feed = db.select(
                """
                select actor_name, verb, object_id, object_type, target_name, time from activities where actor_id in (
                    SELECT  unnest(follow_ids) from users WHERE id = ?
                )
                """,
                [current_user['id']]
            )

            content = {
                "friends_feed": friends_feed,
                "next_url": ""
            }
            return content, 200

        except Exception as e:
            app.logger.error(e)
            content = {
                "error": True,
                "message": "Something wrong on our side, sorry"
            }
            return content, 500
