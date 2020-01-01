import pytest
from users.models import CustomUser
from rest_framework.test import APIClient, APIRequestFactory
import json
import pathlib, smtplib


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
@pytest.fixture
def add_news_fixtures(request):
    # # smtp = request.param
    # # print(smtp)
    # smtp = smtplib.SMTP(request.param)
    #
    # def fin():
    #     print("finalizing %s" % smtp)
    #     smtp.close()
    #
    # request.addfinalizer(fin)
    # print(smtp)
    # return smtp
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.with_name('add_news.json')
    with config.open() as fp:
        return json.load(fp)

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


