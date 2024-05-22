import unittest
from flask import current_app
from app import create_app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload Excel para BigQuery', response.data)

if __name__ == '__main__':
    unittest.main()
