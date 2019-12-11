from django.urls import path
from .views import Index, SignUpApiView, LoginApiView

urlpatterns = [

    path('', Index.as_view(), name='index'),
    path('registration/', SignUpApiView.as_view(), name='registration'),
    path('login/', LoginApiView.as_view(), name='login')
]