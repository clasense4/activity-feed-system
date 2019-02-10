from flask_testing import TestCase
import unittest
from main import app as flask_app
import json

class test_1_post(TestCase):
    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def test_1a_post_activity_correct_request_post(self):
        response = self.client.post(
                                    '/post',
                                    data=json.dumps({
                                        "type": "post",
                                        "content":"{\"foo\":\"bar\"}"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['type'], 'post')
        self.assertEqual(response.json['message'], 'Activity recorded')

    def test_1b_post_activity_correct_request_photo(self):
        response = self.client.post(
                                    '/post',
                                    data=json.dumps({
                                        "type": "photo",
                                        "content":"fajri.jpeg"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['type'], 'photo')
        self.assertEqual(response.json['message'], 'Activity recorded')

    def test_2a_post_activity_type_missing(self):
        response = self.client.post(
                                    '/post',
                                    data=json.dumps({
                                        "content":"fajri.jpeg"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Type is missing or not valid')

    def test_2b_post_activity_type_is_not_valid(self):
        response = self.client.post(
                                    '/post',
                                    data=json.dumps({
                                        "type": "photosss",
                                        "content":"fajri.jpeg"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Type is missing or not valid')

    def test_2c_post_activity_content_is_missing(self):
        response = self.client.post(
                                    '/post',
                                    data=json.dumps({
                                        "type": "photo"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Content is missing')

if __name__ == '__main__':
    unittest.main()