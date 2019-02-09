from flask_testing import TestCase
import unittest
from main import app as flask_app
import json

class test_follow(TestCase):
    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def test_1a_post_follow_correct(self):
        response = self.client.post(
                                    '/follow',
                                    data=json.dumps({
                                        "follow":"eric"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'follow')
        self.assertEqual(response.json['message'], 'User followed')

    def test_1b_post_follow_correct(self):
        response = self.client.post(
                                    '/follow',
                                    data=json.dumps({
                                        "follow":"eric"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'follow')
        self.assertEqual(response.json['message'], 'Already followed')

    def test_2a_post_follow_wrong_user(self):
        response = self.client.post(
                                    '/follow',
                                    data=json.dumps({
                                        "follow":"`;dadang"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'User not found')

    def test_2b_post_follow_wrong_same_user(self):
        """ivan want to follow ivan"""
        response = self.client.post(
                                    '/follow',
                                    data=json.dumps({
                                        "follow":"ivan"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'You can\'t follow yourself')

if __name__ == '__main__':
    unittest.main()