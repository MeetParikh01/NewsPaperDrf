import pytest, json
from rest_framework import status
from users.models import CustomUser
from users.views import *
from mixer.backend.django import mixer
from django.urls import reverse
from rest_framework.test import force_authenticate
from django.conf import settings
from importlib import import_module
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
        view = LogoutApiView.as_view()
        url = reverse('logout')
        request = api_request_factory.get(url)
        # force_authenticate(request, user=user)
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.user = mixer.blend('users.CustomUser')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestProfileApiView:

    def test_retrieve_profile(self, request, api_request_factory):
        view = ProfileApiView.as_view()
        url = reverse('profile', kwargs={'pk':1})
        request = api_request_factory.get(url)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=1)
        assert response.status_code == status.HTTP_200_OK
        assert response.template_name == 'users/profile_detail.html'



