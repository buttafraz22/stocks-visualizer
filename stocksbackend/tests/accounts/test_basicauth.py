from django.urls import reverse
from django.contrib.auth.models import User

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token



def create_user_token(username, password):

    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)
    return token


@pytest.mark.django_db(transaction=True)
def test_no_bearer_token():
    
    # Test the API when there is no bearer token. Expect
    # to be denied.

    endpoint = reverse('symbol-stats')
    client = APIClient()
    res = client.get(endpoint)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in res.data
    assert res.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db(transaction=True)
def test_protected_api_authenticated():

    endpoint = reverse('symbol-stats')
    token = create_user_token('testuser', 'testpass')

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.key}')
    
    res = client.get(endpoint)

    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_wrong_credentials():

    # Login in wrong password

    endpoint = reverse('login')
    token = create_user_token(username='testuser', password='testpass')
    client = APIClient()

    payload = {
        "username" : "testuser",
        "password" : "Some Wrong Password"
    }
    res = client.post(endpoint, payload, format='json')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # Login in wrong username

    payload = {
        "username" : "some wrong username",
        "password" : "testpass"
    }
    res = client.post(endpoint, payload, format='json')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


    

