import pytest
from users.models import CustomUser
from news_categories.models import *
from rest_framework.test import APIClient, APIRequestFactory
import json, pathlib, smtplib
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO, StringIO
from PIL import Image
from mixer.backend.django import mixer
from rest_framework_jwt.settings import api_settings



def load_params_from_json(json_path):
    with open(json_path) as f:
        return json.load(f)


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


# @pytest.fixture( params=load_params_from_json('/home/botree/python/add_news.json'))
# @pytest.fixture
# def add_news_fixtures(request):
#     # # smtp = request.param
#     # # print(smtp)
#     # smtp = smtplib.SMTP(request.param)
#     #
#     # def fin():
#     #     print("finalizing %s" % smtp)
#     #     smtp.close()
#     #
#     # request.addfinalizer(fin)
#     # print(smtp)
#     # return smtp
#     file = pathlib.Path(request.node.fspath.strpath)
#     config = file.with_name('add_news.json')
#     with config.open() as fp:
#         add_news_data = json.load(fp)
#     for data in add_news_data:
#         image = BytesIO()
#         Image.new('RGB', (100, 100)).save(image, 'JPEG')
#         image.seek(0)
#         AddNewsModel.objects.create(news_title=data.get('fields').get('news_title'),
#                                     news_body=data.get('fields').get('news_body'),
#                                     news_category=mixer.blend('news_categories.NewCategoriesModel'),
#                                     user=mixer.blend('users.CustomUser'),
#                                     image=SimpleUploadedFile('image.jpg', image.getvalue()))
#     return AddNewsModel.objects.all()

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def news_modify():
    category = mixer.blend('news_categories.NewCategoriesModel', pk=4)
    news = mixer.blend('news_categories.AddNewsModel', id=2, news_category=category)
    return news


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


@pytest.fixture
def temp_image():
    image = BytesIO()
    Image.new('RGB', (100, 100)).save(image, 'JPEG')
    image.seek(0)
    return SimpleUploadedFile('image.jpg', image.getvalue())


@pytest.fixture
def token():
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user = mixer.blend('users.CustomUser', id=1)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token, user