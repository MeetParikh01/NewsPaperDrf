import tempfile
import pytest,datetime
from rest_framework import status
from mixer.backend.django import mixer
from django.urls import reverse
from rest_framework.test import force_authenticate
from django.conf import settings
from importlib import import_module
from news_categories.views import *
from io import BytesIO, StringIO
from PIL import Image
from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestAddNewsApiView:

    def test_get_add_news_form(self,api_request_factory):
        view = AddNewsApiView.as_view()
        url = reverse('add_news')
        request = api_request_factory.get(url)
        request.user = mixer.blend('users.CustomUser')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_post_valid_add_news_form(self,api_request_factory):
        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'JPEG')
        image.seek(0)

        # Second method to create image
            # image = Image.new('RGB', (100, 100))
            # tmp_file = tempfile.NamedTemporaryFile(suffix='.jpeg')
            # image.save(tmp_file)
            # with open(tmp_file.name, 'rb') as file:
        data = {
            'news_title': 12345,
            'news_body': 'this is news body',
            'news_category': mixer.blend('news_categories.NewCategoriesModel', category_name='mobile').id,
            'date': datetime.datetime.now(),
            'image': SimpleUploadedFile('image.jpg', image.getvalue())
        }
        view = AddNewsApiView.as_view()
        url = reverse('add_news')
        request = api_request_factory.post(url, data=data, format='multipart')
        request.user = mixer.blend('users.CustomUser')
        response = view(request)
        assert response.status_code == status.HTTP_302_FOUND

    def test_post_invalid_add_news_form(self, api_request_factory):
        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'JPEG')
        image.seek(0)

        data = {


            'news_category': mixer.blend('news_categories.NewCategoriesModel', category_name='mobile').id,
            'date': datetime.datetime.now(),
            'image': SimpleUploadedFile('image.jpg', image.getvalue())
        }
        view = AddNewsApiView.as_view()
        url = reverse('add_news')
        request = api_request_factory.post(url, data=data, format='multipart')
        request.user = mixer.blend('users.CustomUser')
        response = view(request)
        assert response.data.get('news_title')[0] == 'This field is required.'
        assert response.data.get('news_body')[0] == 'This field is required.'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

class TestNewsDisplay:

    def test_get_news(self,api_client, add_news_fixtures):
        print('------------------------')
        for i in add_news_fixtures:
            print(i.get('pk'))
        pass