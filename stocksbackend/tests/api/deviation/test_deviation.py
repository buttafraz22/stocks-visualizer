from django.urls import reverse

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .fixtures import generate_dummy_stock_data
from ...utils import create_user_token, create_api_client

class TestDeviationAPI:
    endpoint = reverse('symbols-deviation')
    date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    

    @pytest.mark.django_db(transaction=True)
    def test_deviation_simple(self, generate_dummy_stock_data):

        token = create_user_token('username', 'userpassword')
        client = create_api_client(token)
        
        response = client.get(f'{self.endpoint}?from={self.date}&to={self.date}&name=Arbisoft')

        assert response.status_code == status.HTTP_200_OK

    
    @pytest.mark.django_db(transaction=True)
    def test_deviation_multiple(self, generate_dummy_stock_data):
        
        token = create_user_token('username', 'userpassword')
        client = create_api_client(token)
       
        response = client.get(f'{self.endpoint}?from={self.date}&to={self.date}&name=Arbisoft%2CHirenze')

        assert response.status_code == status.HTTP_200_OK
    
    
    @pytest.mark.django_db(transaction=True)
    def test_deviation_missing_dates(self, generate_dummy_stock_data):

        token = create_user_token('username', 'userpassword')
        client = create_api_client(token)

        # I missed the 'to' argument needed by the server.
        response = client.get(f'{self.endpoint}?from={self.date}&name=Arbisoft%2CHirenze')
        assert response.status_code == 400

        # I missed the 'from' argument needed by the server.
        response = client.get(f'{self.endpoint}?to={self.date}&name=Arbisoft%2CMillerson')
        assert response.status_code == 400


    @pytest.mark.django_db(transaction=True)
    def test_deviation_missing_company(self, generate_dummy_stock_data):
        
        token = create_user_token('username', 'userpassword')
        client = create_api_client(token)

        response = client.get(f'{self.endpoint}?from={self.date}&to={self.date}')
        assert response.status_code == 404