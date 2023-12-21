import unittest
from flask import Flask

import views

app = views.app

class Test(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()