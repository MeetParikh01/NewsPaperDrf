from django.urls import path
from .views import IndexApiView, SignUpApiView, LoginApiView

urlpatterns = [

    path('', IndexApiView.as_view(), name='index'),
    path('registration/', SignUpApiView.as_view(), name='registration'),
    path('login/', LoginApiView.as_view(), name='login')
]