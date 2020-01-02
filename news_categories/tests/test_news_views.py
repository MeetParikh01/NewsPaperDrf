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


@pytest.mark.django_db
class TestNewsDetailApiView:

    def test_get_news_detail(self, api_request_factory):
        view = NewsDetailApiView.as_view()
        url = reverse('news_detail', kwargs={'pk':2})
        request = api_request_factory.get(url)
        category = mixer.blend('news_categories.NewCategoriesModel', pk=4)
        news = mixer.blend('news_categories.AddNewsModel', id=2, news_category=category)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=2)
        assert response.status_code == status.HTTP_200_OK
        assert news.news_title == response.data.get('news_detail').get('news_title')


@pytest.mark.django_db
class TestNewsCategoryApiView:

    def test_get_news_category(self, api_request_factory):
        view = NewsCategoryApiView.as_view()
        url = reverse('news_category', kwargs={'pk': 4})
        request = api_request_factory.get(url)
        category = mixer.blend('news_categories.NewCategoriesModel', pk=4)
        news = mixer.blend('news_categories.AddNewsModel', id=2, news_category=category)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=4)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestNewsPostedByUserApiView:

    def test_get_news_by_user(self, api_request_factory):
        view = NewsPostedByUserApiView.as_view()
        url = reverse('news_postedby_user')
        request = api_request_factory.get(url)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request)
        assert response.template_name == 'news_categories/news_postedby_user.html'
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestNewsEditOrDeletePostedByUserApiView:

    def test_retrieve_news_by_user(self, api_request_factory, news_modify):
        view = NewsEditOrDeletePostedByUserApiView.as_view()
        url = reverse('news_modify_byuser', kwargs={'pk': news_modify.id})
        request = api_request_factory.get(url)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=news_modify.id)
        assert response.template_name == 'news_categories/news_post_update.html'
        assert response.status_code == status.HTTP_200_OK

    def test_update_valid_news_by_user(self, api_request_factory, news_modify, temp_image):
        view = NewsEditOrDeletePostedByUserApiView.as_view()
        url = reverse('news_modify_byuser', kwargs={'pk': news_modify.id})
        category = mixer.blend('news_categories.NewCategoriesModel', pk=5)
        data = {
            'news_title': 'updated title',
            'news_body': 'updated body',
            'image': temp_image,
            'news_category': category.id
        }
        request = api_request_factory.put(url, data=data)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=news_modify.id)
        data = eval(response.content.decode('utf-8'))
        assert data.get('status') == 'success'
        assert response.status_code == status.HTTP_200_OK

    def test_update_invalid_news_by_user(self, api_request_factory, news_modify, temp_image):
        view = NewsEditOrDeletePostedByUserApiView.as_view()
        url = reverse('news_modify_byuser', kwargs={'pk': news_modify.id})
        data = {
            'news_title': 'updated title',
            'news_body': 'updated body',
            'image': temp_image,
            'news_category': 'category.id'
        }
        request = api_request_factory.put(url, data=data)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=news_modify.id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_news_by_user(self,api_request_factory, news_modify):
        view = NewsEditOrDeletePostedByUserApiView.as_view()
        url = reverse('news_modify_byuser', kwargs={'pk': news_modify.id})
        request = api_request_factory.delete(url)
        request.user = mixer.blend('users.CustomUser', pk=1)
        response = view(request, pk=news_modify.id)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDuplicateNewsPostedByUserApiView:

    def test_get_duplicate_news_by_user(self, api_request_factory, token):
        bearer_token, user = token
        token = 'Bearer '+bearer_token
        print(token)
        view = NewsPostedByUserApiView.as_view()
        url = reverse('news_postedby_user')
        request = api_request_factory.get(url)
        force_authenticate(request, user=user, token=token)
        response = view(request)
        assert response.template_name == 'news_categories/news_postedby_user.html'
        assert response.status_code == status.HTTP_200_OK
