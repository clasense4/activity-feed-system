import json
from config.bootstrap import app, db
from decorators.headers import valid_token, valid_json
from flask import g, request
from IPython import embed

class controller:
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