import pytest
from mixer.backend.django import mixer
from news_categories.models import *


@pytest.mark.django_db
class TestNewCategoriesModel:

    def test_isinstance_news_category(self):
        news = mixer.blend('news_categories.NewCategoriesModel', category_name='cricket')
        assert isinstance(news, NewCategoriesModel)

    def test_news_category_name(self):
        news = mixer.blend('news_categories.NewCategoriesModel', category_name='cricket')
        assert news.category_name == 'cricket'


@pytest.mark.django_db
class TestAddNewsModel:

    def test_isinstance_news_category(self):
        add_news = mixer.blend('news_categories.AddNewsModel')
        assert isinstance(add_news, AddNewsModel)

    def test_add_news(self):
        add_news = mixer.blend('news_categories.AddNewsModel')
        assert add_news.image == 'default.jpeg'