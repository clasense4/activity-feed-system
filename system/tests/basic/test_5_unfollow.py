from flask_testing import TestCase
import unittest
from main import app as flask_app
import json

class test_5_unfollow(TestCase):
    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def test_1a_post_unfollow_correct(self):
        response = self.client.post(
                                    '/unfollow',
                                    data=json.dumps({
                                        "unfollow":"eric"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'unfollow')
        self.assertEqual(response.json['message'], 'User unfollowed')

    def test_2a_post_follow_wrong_user(self):
        response = self.client.post(
                                    '/unfollow',
                                    data=json.dumps({
                                        "unfollow":"`;dadang"
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
                                    '/unfollow',
                                    data=json.dumps({
                                        "unfollow":"ivan"
                                    }),
                                    headers={"X-App-Key": "abc123"},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], True)
        self.assertEqual(response.json['message'], 'You can\'t unfollow yourself')

if __name__ == '__main__':
    unittest.main()