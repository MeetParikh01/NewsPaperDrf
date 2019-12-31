from django.urls import reverse, resolve


class TestUrls:
    def test_profile_url(self):
        path = reverse('profile', kwargs={'pk': 1})
        assert resolve(path).view_name == 'profile'


