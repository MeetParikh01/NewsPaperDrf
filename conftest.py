import pytest
from users.models import CustomUser
from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture
def user():
    return CustomUser.objects.create(username='meet',
                                     first_name='meet',
                                     last_name='parikh',
                                     password='botree123',
                                     email='meet.parikh@botreetechnologies.com',
                                     contact='985621',
                                     address='asdf',
                                     pincode=123456)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


