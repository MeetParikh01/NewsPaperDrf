from django.test import TestCase
from users.models import CustomUser
import pytest
from mixer.backend.django import mixer


# Create your tests here.


@pytest.mark.django_db
def test_my_user(user):
    assert user.is_superuser == False


# pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestCustomUserModels:

    def test_isinstance(self, user):
        assert isinstance(user, CustomUser)

    def test_user_is_active(self):
        user = mixer.blend('users.CustomUser', is_active=True)
        assert user.is_active

    def test_check_email(self, user):
        assert user.email != 'meet.@botreetechnologies.com'



