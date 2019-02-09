from flask_testing import TestCase
import unittest
from main import app as flask_app
import json

class test_activity(TestCase):
    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def test_1a_post_activity_correct_request_post(self):
        response = self.client.post(
                                    '/activity',
                                    data=json.dumps({
                                        "actor":"ivan",
                                        "verb":"post",
                                        "object":"photo:2"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'post')
        self.assertEqual(response.json['message'], 'Activity recorded')

    def test_1b_post_activity_correct_request_post(self):
        response = self.client.post(
                                    '/activity',
                                    data=json.dumps({
                                        "actor":"nico",
                                        "verb":"post",
                                        "object":"photo:3"
                                    }),
                                    headers={"X-App-Key": "abc124"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'post')
        self.assertEqual(response.json['message'], 'Activity recorded')

    def test_1c_post_activity_correct_request_ignore_target(self):
        response = self.client.post(
                                    '/activity',
                                    data=json.dumps({
                                        "actor":"nico",
                                        "verb":"post",
                                        "object":"photo:4",
                                        "target":"ivan"
                                    }),
                                    headers={"X-App-Key": "abc124"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'post')
        self.assertEqual(response.json['message'], 'Activity recorded')

    def test_2a_post_activity_wrong_object_format(self):
        response = self.client.post(
                                    '/activity',
                                    data=json.dumps({
                                        "actor":"ivan",
                                        "verb":"post",
                                        "object":"photo:x"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Wrong object format')

    # Cover : valid_json@headers.py
    def test_2a_post_activity_request_is_not_json(self):
        response = self.client.post(
                                    '/activity',
                                    data={
                                        "actor":"ivan",
                                        "verb":"post",
                                        "object":"photo:2",
                                        "target":"eric"
                                    },
                                    headers={"X-App-Key": "abc123"}
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Must be json request')


    # Cover : valid_json@headers.py
    def test_2b_post_activity_request_is_json_headers_wrong_body_format(self):
        response = self.client.post(
                                    '/activity',
                                    data={
                                        "actor":"ivan",
                                        "verb":"post",
                                        "object":"photo:2",
                                        "target":"eric"
                                    },
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Bad Request')

    def test_3_post_activity_verb_is_not_valid(self):
        response = self.client.post(
                                    '/activity',
                                    data=json.dumps({
                                        "actor":"ivan",
                                        "verb":"",
                                        "object":"photo:2",
                                        "target":"eric"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Wrong verb format')

    def test_4_post_activity_wrong_object_format(self):
        response = self.client.post(
                                    '/activity',
                                    data=json.dumps({
                                        "actor":"ivan",
                                        "verb":"post",
                                        "object":"x:2",
                                        "target":"eric"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Wrong object format')


if __name__ == '__main__':
    unittest.main()