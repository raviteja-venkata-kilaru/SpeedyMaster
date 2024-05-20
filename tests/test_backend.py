import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_product(self):
        response = self.app.post('/api/createProducts', json={'name': 'Test Product', 'price': 10.99})
        self.assertEqual(response.status_code, 201)

    def test_get_product(self):
        response = self.app.get('/api/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Product')

if __name__ == '__main__':
    unittest.main()


