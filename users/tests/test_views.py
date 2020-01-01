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

    def test_retrieve_profile(self, api_request_factory):
        view = ProfileApiView.as_view()
        url = reverse('profile', kwargs={'pk':1})
        request = api_request_factory.get(url)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=1)
        assert response.status_code == status.HTTP_200_OK
        assert response.template_name == 'users/profile_detail.html'


@pytest.mark.django_db
class TestSignUpApiView:
    data = [
        ('meet', 'meet', 'parikh', 'botree123', 'botree123',
         'meet.parikh@botreetechnologies.com', '789456', 'absckcsa', 123456),

        ('xyz', 'xyz', 'parikh', 'botree123', 'botree123',
         'meet.parikh@botreetechnologies.com', '789456', 'absckcsa', 123456),

    ]

    @pytest.mark.parametrize('username,first_name,last_name,password,confirm_password,'
                             'email,contact,address,pincode', data)
    def test_post_valid_sign_up(self, username,first_name,last_name,password,confirm_password,
                                email,contact,address,pincode,api_client):
        url = reverse('registration')
        data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'confirm_password': password,
            'email': email,
            'contact': contact,
            'address': address,
            'pincode': pincode,
        }
        response = api_client.post(url, data=data)

        assert response.status_code == 302

    def test_post_invalid_sign_up(self, user, api_client):
        url = reverse('registration')
        data = {
            'username': 'user.username',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': user.password,
            'confirm_password': 123456,
            'email': 'abc@gmail.com',
            'contact': user.contact,
            'address': user.address,
            'pincode': user.pincode,
        }
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_sign_up(self,user, api_client):
        url = reverse('registration')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestProfileDetailApiView:

    def test_retrieve_profile_update_data(self, api_request_factory):
        view = ProfileDetailApiView.as_view()
        url = reverse('profileupdate', kwargs={'pk': 1})
        request = api_request_factory.get(url)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=1)
        assert response.status_code == status.HTTP_200_OK

    def test_put_valid_profile_update_data(self, api_request_factory, user):
        data = {
            'username': 'user.username',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': 'abc@gmail.com',
            'contact': '123456',
            'address': user.address,
            'pincode': user.pincode,
        }
        view = ProfileDetailApiView.as_view()
        url = reverse('profileupdate', kwargs={'pk': user.id})
        request = api_request_factory.put(url, data=data)
        force_authenticate(request, user=user)
        response = view(request, pk=user.id)
        assert response.status_code == status.HTTP_200_OK

    def test_put_invalid_profile_update_data(self, api_request_factory, user):
        data = {
            'username': user.username,

            'last_name': user.last_name,
            'email': 'abc@gmail.com',
            'contact': '123456789101112',
            'address': user.address,
            'pincode': 'ckjbkjcbkj',
        }
        view = ProfileDetailApiView.as_view()
        url = reverse('profileupdate', kwargs={'pk': user.id})
        request = api_request_factory.put(url, data=data)
        force_authenticate(request, user=user)
        response = view(request, pk=user.id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_profile(self, user, api_request_factory):
        view = ProfileDetailApiView.as_view()
        url = reverse('profileupdate', kwargs={'pk': user.id})
        request = api_request_factory.delete(url)
        force_authenticate(request, user=user)
        response = view(request, pk=user.id)
        assert response.status_code == status.HTTP_200_OK


