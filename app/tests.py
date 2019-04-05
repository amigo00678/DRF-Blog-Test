import json
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from app.models import BlogPost


class UsersTest(TestCase):
    """
    Test users URLs
    """
    def setUp(self):
        self.users = []
        self.users.append(User.objects.create_user(
            username='testUser1', email='user1@u.com', password='top_secret'))
        self.users.append(User.objects.create_user(
            username='testUser2', email='user1@u.com', password='top_secret'))

    def test_list_users(self):
        """
        Test list users
        """
        client = APIClient()
        response = client.get('/users/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['count'], 2)
        userNames = [user.username for user in self.users]
        for user in data['results']:
            self.assertIn(user['username'], userNames)

    def test_list_users_sorting(self):
        """
        Test list users with sorting
        """
        client = APIClient()
        response = client.get('/users/?orderig=asc')
        self.assertEqual(response.status_code, 200)

    def test_user_details(self):
        """
        Test show user
        """
        client = APIClient()
        for user in self.users:
            response = client.get('/users/{}/'.format(user.id))
            self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        """
        Test add user
        """
        client = APIClient()
        response = client.post('/users/',
            {'password': 'password123', 'username': 'userXX', 'email': 'ux@uu.com'},
            headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 201)
        response = client.post('/users/',
            {'password': 'password123', 'username': 'userYY', 'email': 'uy@uu.com'},
            headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 201)


class AuthTest(TestCase):
    """
    Test authorization URLs
    """
    def setUp(self):
        self.users = []
        self.users.append(User.objects.create_user(
            username='testUser1', email='user1@u.com', password='top_secret'))

    def test_auth(self):
        """
        Test getting authorization token
        """
        client = APIClient()
        response = client.post('/token-auth/',
            {'username': 'testUser1', 'password': 'top_secret'},
            headers={'content-type': 'application/json'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_auth_error(self):
        """
        Test authorization error
        """
        client = APIClient()
        response = client.post('/token-auth/',
            {'username': 'testUser1', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 400)

    def test_token_refresh(self):
        """
        Test refresh authorization token
        """
        client = APIClient()
        response = client.post('/token-auth/',
            {'username': 'testUser1', 'password': 'top_secret'})
        self.assertEqual(response.status_code, 200)

        response = client.post('/token-refresh/',
            {'token': response.json()['token']})
        self.assertEqual(response.status_code, 200)

    def test_token_refresh_error(self):
        """
        Test refresh token error
        """
        client = APIClient()
        response = client.post('/token-auth/',
            {'username': 'testUser1', 'password': 'top_secret'})
        self.assertEqual(response.status_code, 200)

        response = client.post('/token-refresh/',
            {'token': response.json()['token']+'blah'})
        self.assertEqual(response.status_code, 400)

    def test_verify_token(self):
        """
        Test verify token
        """
        client = APIClient()
        response = client.post('/token-auth/',
            {'username': 'testUser1', 'password': 'top_secret'})
        self.assertEqual(response.status_code, 200)

        response = client.post('/token-verify/',
            {'token': response.json()['token']})
        self.assertEqual(response.status_code, 200)

    def test_verify_token_error(self):
        """
        Test verify token error
        """
        client = APIClient()
        response = client.post('/token-auth/',
            {'username': 'testUser1', 'password': 'top_secret'})
        self.assertEqual(response.status_code, 200)

        response = client.post('/token-verify/',
            {'token': response.json()['token']+'blah'})
        self.assertEqual(response.status_code, 400)


class BlogPostTest(TestCase):
    """
    Test blog posts URLs
    """
    def setUp(self):
        self.users = []
        self.users.append(User.objects.create_user(
            username='testUser1', email='user1@u.com', password='top_secret'))
        self.posts = []
        self.posts.append(BlogPost.objects.create(
            title='Test Title 1', body='Test body 1', owner=self.users[0]))

        client = APIClient()
        response = client.post('/token-auth/',
            {'username': 'testUser1', 'password': 'top_secret'},
            headers={'content-type': 'application/json'})

        self.token = response.json()['token']

    def test_posts_list(self):
        """
        Test list of posts
        """
        client = APIClient()
        response = client.get('/posts/')

        self.assertEqual(response.status_code, 200)

    def test_post_details(self):
        """
        Test show post details
        """
        client = APIClient()
        post = self.posts[0]
        response = client.get('/posts/{}/'.format(post.id))
        self.assertEqual(response.status_code, 200)

    def test_post_add(self):
        """
        Test add post
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.post('/posts/',
            {'title': 'Test Title 2', 'body': 'Test body 2'})
        self.assertEqual(response.status_code, 201)

    def test_post_add_error(self):
        """
        Test add post with authorization error
        """
        client = APIClient()
        response = client.post('/posts/',
            {'title': 'Test Title 3', 'body': 'Test body 3'})
        self.assertEqual(response.status_code, 401)
