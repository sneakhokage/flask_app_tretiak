import unittest
from app import app 

class ProductsBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_all_products_page(self):
        """Тест маршруту /products/."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)

      
        data = response.get_data(as_text=True)

    
        self.assertIn("Ноутбук", data)
        self.assertIn("Клавіатура", data)

    def test_product_details_page(self):
        """Тест маршруту /products/<id>."""
        response = self.client.get("/products/123")
        self.assertEqual(response.status_code, 200)

    
        data = response.get_data(as_text=True)

      
        self.assertIn("123", data)
        self.assertIn("Деталі для продукту", data)

if __name__ == "__main__":
    unittest.main()