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


if __name__ == '__main__':
    unittest.main()