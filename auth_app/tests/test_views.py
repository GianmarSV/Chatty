import pytest
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.management import call_command
from io import StringIO

User = get_user_model()


@pytest.fixture(scope='session')
def create_superuser(django_db_setup, django_db_blocker):
    # Prepare superuser data
    username = 'admin'
    email = 'admin@example.com'
    password = 'adminpassword'

    # Create the superuser using Django's ORM
    with django_db_blocker.unblock():
        user = User.objects.create_superuser(username=username, email=email, password=password)

@pytest.mark.django_db
def test_signup_view(create_superuser):
    client = APIClient()
    url = reverse('signup')
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_signup_view_invalid_data(create_superuser):
    client = APIClient()
    url = reverse('signup')
    data = {}  # Invalid data
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_signin_view(create_superuser):
    client = APIClient()
    url = reverse('signin')
    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_signin_view_invalid_data(create_superuser):
    client = APIClient()
    url = reverse('signin')
    data = {}  # Invalid data
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
