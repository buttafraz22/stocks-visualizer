import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

def create_user_token(username:str, password:str) -> Token:
    """Creates a dummy user for testing purposes in the lifecycle.
    User credentials will vanish once the test cycle is over.

    Args:
        username (str): The username of the said user.
        password (str): The password of the said user.

    Returns:
        str : The token generated on the virtual server.
    """
    user = User.objects.create_user(username, password)
    token = Token.objects.create(user=user)
    return token

@pytest.mark.django_db(transaction=True)
def create_api_client(auth_token:str)->APIClient:
    """Creates the RESTful API client that the test will consume.

    Args:
        auth_token (str): The token of the user that acts as an authorization
        mechanism for the RESTful client. By convention, this 
        has a structure of Bearer {your-token-value}. This value will
        be passed as the auth_token argument.

    Returns:
        APIClient: The validated API Client of the testing mechanism.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
    return client