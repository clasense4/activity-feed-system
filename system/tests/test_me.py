from flask_testing import TestCase
import unittest
from main import app as flask_app
# from nose.tools import set_trace
import json

class test_me(TestCase):
    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def test_1_get_me_correct_credentials(self):
        response = self.client.get(
                                    '/me',
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'ivan')

    def test_2_get_me_failure_credentials(self):
        response = self.client.get(
                                    '/me',
                                    headers={"X-App-Key": "abc123x"},
                                    content_type='application/json'
                                )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Key is not valid')

    def test_3_get_me_key_empty(self):
        response = self.client.get(
                                    '/me',
                                    headers={"X-App-Key": ""},
                                    content_type='application/json'
                                )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Key is not valid')

    def test_4_get_me_no_headers(self):
        response = self.client.get(
                                    '/me',
                                    content_type='application/json'
                                )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'Key is missing')

if __name__ == '__main__':
    unittest.main()