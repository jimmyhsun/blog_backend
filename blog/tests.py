import pytest
from blog.models import User, Post
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_success():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')

    response = client.post('/api/v1/login', {
        'username': 'testuser',
        'password': 'testpass'
    }, format='json')

    assert response.status_code == 200
    assert 'access_token' in response.data
    assert 'refresh_token' in response.data


@pytest.mark.django_db
def test_login_fail():
    client = APIClient()
    response = client.post('/api/v1/login', {
        'username': 'wronguser',
        'password': 'wrongpass'
    }, format='json')

    assert response.status_code == 401


@pytest.mark.django_db
def test_reader_cannot_update_post():
    client = APIClient()

    author = User.objects.create_user(username='author', password='authorpass', role='author')
    reader = User.objects.create_user(username='reader', password='readerpass', role='reader')

    post = Post.objects.create(author=author, title='Author Title', content='Author Content')

    login_resp = client.post('/api/v1/login', {
        'username': 'reader',
        'password': 'readerpass'
    }, format='json')

    access_token = login_resp.data['access_token']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')


    response = client.put(f'/api/v1/posts/{post.id}', {
        'title': 'Hacked Title',
        'content': 'Hacked Content',
    }, format='json')

    assert response.status_code == 403



@pytest.mark.django_db
def test_create_post_with_token():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')

    login_resp = client.post('/api/v1/login', {
        'username': 'testuser',
        'password': 'testpass'
    }, format='json')

    access_token = login_resp.data['access_token']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    response = client.post('/api/v1/posts', {
        'title': 'New Title',
        'content': 'New Content',
    }, format='json')

    assert response.status_code == 201
    assert response.data['title'] == 'New Title'
