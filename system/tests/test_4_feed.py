from flask_testing import TestCase
import unittest
from main import app as flask_app
import json
from IPython import embed

class test_4_feed(TestCase):
    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def test_1a_ivan_feed(self):
        response = self.client.get(
                                    '/feed/my',
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['my_feed']), 6)


    def test_2a_ivan_friends_feed(self):
        response = self.client.get(
                                    '/feed/friends',
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.json['my_feed']), 6)
