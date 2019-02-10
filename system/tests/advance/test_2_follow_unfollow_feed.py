from flask_testing import TestCase
import unittest
from main import app as flask_app
import json

IVAN = "abc123"
NICO = "abc124"
ERIC = "abc125"

class test_2_follow_unfollow_feed(TestCase):

    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        return app

    def test_1a_post_ivan_post_10(self):
        """
        IVAN Create 5 post, 5 photo
        """
        for i in range(10):
            post_type = "photo" if i > 4 else "post"

            response = self.client.post(
                                        '/post',
                                        data=json.dumps({
                                            "type": post_type,
                                            "content":"content1"
                                        }),
                                        headers={"X-App-Key": IVAN},
                                        content_type='application/json'
                                    )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['type'], post_type)
            self.assertEqual(response.json['message'], 'Activity recorded')

    def test_1b_check_ivan_feed(self):
        """
        Check IVAN's feed, has 10 post
        """
        response = self.client.get(
                            '/feed/my',
                            headers={"X-App-Key": IVAN},
                            content_type='application/json'
                        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['my_feed']), 10)

    def test_2a_post_eric_post_10(self):
        """
        ERIC Create 5 post, 5 photo
        """
        for i in range(10):
            post_type = "photo" if i > 4 else "post"

            response = self.client.post(
                                        '/post',
                                        data=json.dumps({
                                            "type": post_type,
                                            "content":"content2"
                                        }),
                                        headers={"X-App-Key": ERIC},
                                        content_type='application/json'
                                    )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['type'], post_type)
            self.assertEqual(response.json['message'], 'Activity recorded')

    def test_2b_check_eric_feed(self):
        """
        Check ERIC's feed, has 10 post
        """
        response = self.client.get(
                            '/feed/my',
                            headers={"X-App-Key": ERIC},
                            content_type='application/json'
                        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['my_feed']), 10)

    def test_3a_post_nico_post_10(self):
        """
        ERIC Create 10 post, 10 photo
        """
        for i in range(20):
            post_type = "photo" if i > 9 else "post"

            response = self.client.post(
                                        '/post',
                                        data=json.dumps({
                                            "type": post_type,
                                            "content":"content2"
                                        }),
                                        headers={"X-App-Key": NICO},
                                        content_type='application/json'
                                    )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['type'], post_type)
            self.assertEqual(response.json['message'], 'Activity recorded')

    def test_3b_check_nico_feed(self):
        """
        Check NICO's feed, has 10 post
        """
        response = self.client.get(
                            '/feed/my',
                            headers={"X-App-Key": NICO},
                            content_type='application/json'
                        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['my_feed']), 20)

    def test_5a_post_follow_ivan_follow_eric(self):
        """
        IVAN following ERIC
        """
        response = self.client.post(
                                    '/follow',
                                    data=json.dumps({
                                        "follow":"eric"
                                    }),
                                    headers={"X-App-Key": IVAN},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'follow')
        self.assertEqual(response.json['message'], 'User followed')

    def test_5b_check_ivan_friends_feed(self):
        """
        Check IVANS's friends feeds, has 10 post (from ERIC)
        """
        response = self.client.get(
                            '/feed/friends',
                            headers={"X-App-Key": IVAN},
                            content_type='application/json'
                        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['friends_feed']), 10)

    def test_6a_post_follow_ivan_follow_nico(self):
        """
        IVAN following NICO
        """
        response = self.client.post(
                                    '/follow',
                                    data=json.dumps({
                                        "follow":"nico"
                                    }),
                                    headers={"X-App-Key": IVAN},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'follow')
        self.assertEqual(response.json['message'], 'User followed')

    def test_6b_check_ivan_friends_feed(self):
        """
        Check IVANS's friends feeds, has 30 post (10 from ERIC, 20 from NICO)
        """
        response = self.client.get(
                            '/feed/friends',
                            headers={"X-App-Key": IVAN},
                            content_type='application/json'
                        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['friends_feed']), 30)

    def test_7a_post_unfollow_ivan_unfollow_eric(self):
        """
        IVAN unfollowing ERIC
        """
        response = self.client.post(
                                    '/unfollow',
                                    data=json.dumps({
                                        "unfollow":"eric"
                                    }),
                                    headers={"X-App-Key": IVAN},
                                    content_type='application/json'
                                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['verb'], 'unfollow')
        self.assertEqual(response.json['message'], 'User unfollowed')

    def test_7b_check_ivan_friends_feed(self):
        """
        Check IVANS's friends feeds, has 20 post (20 from NICO)
        """
        response = self.client.get(
                            '/feed/friends',
                            headers={"X-App-Key": IVAN},
                            content_type='application/json'
                        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['friends_feed']), 20)

if __name__ == '__main__':
    unittest.main()