from django.urls import reverse

import pytest
from rest_framework.test import APIClient
from rest_framework import status

from ...utils import create_user_token


@pytest.mark.django_db(transaction=True)
def test_stats_api():

    endpoint = reverse('symbol-stats')
    token = create_user_token('testuser', 'testpass')

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.key}')
    
    res = client.get(endpoint)

    assert res.status_code == status.HTTP_200_OK