import unittest
from app import app, db
from app.posts.models import Post

class PostModelTestCase(unittest.TestCase):
    
    def setUp(self):
        """
        Налаштування тестового середовища перед кожним тестом.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app_context = app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        self.client = app.test_client()

    def tearDown(self):
        """
        Очищення після кожного тесту.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post_post(self):
        """
        Тест створення поста (POST-запит).
        """
        response = self.client.post(
            '/post/create',
            data={
                'title': 'Тестовий Пост',  
                'content': 'Це вміст тестового поста.',
                'submit': 'Save Post'
            },
            follow_redirects=True
        )
        
        self.assertEqual(response.status_code, 200)

        post = db.session.get(Post, 1)
        self.assertIsNotNone(post)
        self.assertEqual(post.title, 'Тестовий Пост') 


        response_data = response.get_data(as_text=True)
        self.assertIn('Пост успішно створено!', response_data)

    def test_read_posts(self):
        """
        Тест відображення постів (Read).
        """

        test_post = Post(title="Інший Тест", content="Вміст іншого теста")
        db.session.add(test_post)
        db.session.commit()

        response_index = self.client.get('/post/')
        self.assertEqual(response_index.status_code, 200)
 
        response_data = response_index.get_data(as_text=True)
        self.assertIn("Інший Тест", response_data)

        response_detail = self.client.get(f'/post/{test_post.id}')
        self.assertEqual(response_detail.status_code, 200)

        response_data_detail = response_detail.get_data(as_text=True)
        self.assertIn("Вміст іншого теста", response_data_detail)

if __name__ == '__main__':
    unittest.main()