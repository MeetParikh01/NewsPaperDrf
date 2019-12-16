from django.urls import path
from .views import IndexApiView, SignUpApiView, LoginApiView, ProfileApiView, ProfileDetailApiView

urlpatterns = [

    path('', IndexApiView.as_view(), name='index'),
    path('registration/', SignUpApiView.as_view(), name='registration'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('profile/<int:pk>', ProfileApiView.as_view(), name='profile'),
    path('profileupdate/<int:pk>', ProfileDetailApiView.as_view(), name='profileupdate')
]