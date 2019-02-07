import json
from config.bootstrap import app, db
from decorators.headers import valid_token, valid_json
from flask import g, request
from IPython import embed

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

    def valid_object_format(self, request):
        # Validate object, can be null
        #   "object":"photo:1",
        try:
            object_name = request.json['object'].split(":")[0]
            valid_object = ['post', 'photo']
            if object_name not in valid_object:
                raise Exception

            # TODO : Support another type, uuid, integer
            object_id = int(request.json['object'].split(":")[1])

            params = {}
            params['object_id'] = object_id
            params['object_type'] = object_name
            return params
        except Exception as e:
            return False

    def valid_target(self, request):
        try:
            target_name = request.json['target']
            target_user = db.table('users').where('name', target_name).first()
            if target_user is None:
                raise Exception

            params = {}
            params['target_id'] = target_user['id']
            params['target_name'] = target_user['name']
            return params
        except Exception as e:
            return False


    def merge_two_dicts(self, x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z