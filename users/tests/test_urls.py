from django.urls import reverse, resolve

class TestUrls:
    def test_profile_url(self):
        path = reverse('profile', kwargs={'pk': 1})
        assert resolve(path).url_name == 'profile'
        assert resolve(path).view_name == 'profile'

    def test_profile_update_url(self):
        path = reverse('profileupdate', kwargs={'pk': 1})
        assert resolve(path).view_name == 'profileupdate'

    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).view_name == 'index'

