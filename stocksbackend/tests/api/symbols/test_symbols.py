from django.urls import reverse

import pytest
from rest_framework.test import APIClient
from rest_framework import status

from ...utils import create_user_token


class TestSymbolsApi:

    @pytest.mark.django_db(transaction=True)
    def test_symbol_creation(self):

        endpoint = reverse('symbols')
        client = APIClient()
        token = create_user_token('testuser', 'testpass')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        correct_payload = {
            'symbol_code' : 'SME',
            'market_code' : 'REG', # for simplicity I'll keep this throughout
            'symbol_name' : 'Dummy'
        }
        correct_create_res = client.post(endpoint, correct_payload, format='json')
        assert correct_create_res.status_code == status.HTTP_201_CREATED

        missing_params_payload = {
            'symbol_name' : 'Dummy',    # Missed symbol_code
            'market_code' : 'REG'
        } 

        missing_params_res = client.post(endpoint, missing_params_payload, format='json')
        assert missing_params_res.status_code == status.HTTP_406_NOT_ACCEPTABLE

        parameter_valid_payload = {
            'symbol_code' : 'Very Long Code NOT ALLOWED',  # Consistent for all params, tested on one
            'market_code' : 'REG', 
            'symbol_name' : 'Dummy'
        }

        parameter_valid_res = client.post(endpoint, parameter_valid_payload, format='json')
        assert parameter_valid_res.status_code == status.HTTP_406_NOT_ACCEPTABLE

    @pytest.mark.django_db
    def test_symbol_retrieval(self):

        endpoint = reverse('symbols')
        client = APIClient()

        token = create_user_token('testuser', 'testpass')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        correct_payload = {
            'symbol_code' : 'SME',
            'market_code' : 'REG', # for simplicity I'll keep this throughout
            'symbol_name' : 'Dummy'
        }
        client.post(endpoint, correct_payload, format='json')

        correct_query = f'?symbol_code=SME&market_code=REG'
        correct_res = client.get(f'{endpoint}{correct_query}')
        assert correct_res.status_code == status.HTTP_200_OK

        missing_params = f'?symbol_code=SME'
        response_412 = client.get(f'{endpoint}{missing_params}')
        assert response_412.status_code == status.HTTP_412_PRECONDITION_FAILED

        wrong_params = f'?symbol_code=NTO&market_code=REG'
        response_404 = client.get(f'{endpoint}{wrong_params}')
        assert response_404.status_code == status.HTTP_404_NOT_FOUND

        correct_res = client.get(f'{endpoint}')
        assert correct_res.status_code == status.HTTP_200_OK
        assert 'next' in correct_res.data



