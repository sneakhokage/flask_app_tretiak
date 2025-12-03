import unittest
from flask import url_for
from flask_login import current_user
from app import create_app, db, bcrypt
from app.users.models import User

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_auth_pages_load(self):
        """
        1. Перевірка коректного завантаження сторінок реєстрації та входу.
        """
        response_register = self.client.get('/users/register')
        self.assertEqual(response_register.status_code, 200)
        self.assertIn(b'Sign Up', response_register.data) 

        response_login = self.client.get('/users/login')
        self.assertEqual(response_login.status_code, 200)
        self.assertIn(b'Sign In', response_login.data)

    def test_user_registration(self):
        """
        2. Тестування збереження користувача у БД при реєстрації.
        """
        response = self.client.post('/users/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'submit': 'Sign Up'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        user = db.session.query(User).filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

        self.assertNotEqual(user.password, 'password123')
        self.assertTrue(bcrypt.check_password_hash(user.password, 'password123'))

    def test_login_and_logout(self):
        """
        3. Тестування входу і виходу користувача.
        """
        password_hash = bcrypt.generate_password_hash('securepass').decode('utf-8')
        user = User(username='loginuser', email='login@test.com', password=password_hash)
        db.session.add(user)
        db.session.commit()

        response_login = self.client.post('/users/login', data={
            'username': 'loginuser',
            'password': 'securepass',
            'submit': 'Sign In'
        }, follow_redirects=True)

        self.assertEqual(response_login.status_code, 200)
        self.assertIn(b'login@test.com', response_login.data) 

        response_account = self.client.get('/users/account')
        self.assertEqual(response_account.status_code, 200)

        response_logout = self.client.get('/users/logout', follow_redirects=True)
        self.assertEqual(response_logout.status_code, 200)
        self.assertIn(b'Sign In', response_logout.data) 

        response_account_after_logout = self.client.get('/users/account', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response_account_after_logout.data) 

        self.assertIn(b'Sign In', response_account_after_logout.data)

if __name__ == '__main__':
    unittest.main()