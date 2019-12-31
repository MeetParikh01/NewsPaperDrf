import pytest, json
from rest_framework import status
from users.models import CustomUser
from users.views import *
from mixer.backend.django import mixer
from django.urls import reverse
from rest_framework.test import force_authenticate
@pytest.mark.django_db
class TestIndexApiView:

    def test_index_api_view(self, api_client):
        url = reverse('index')
        response = api_client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestLoginApiView:

    def test_get_login(self, api_client):
        url = reverse('login')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_post_login(self, api_client, user):
        url = reverse('login')
        email = user.email
        password = user.password
        data = {'email': email, 'password': password}
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestLogoutApiView:

    def test_logout(self,request, api_request_factory, api_client, user):
        # view = LogoutApiView.as_view()
        url = reverse('logout')
        # request = api_request_factory.get(url)
        # request.user = mixer.blend('users.CustomUser')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK



