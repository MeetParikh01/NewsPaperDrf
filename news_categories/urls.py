from django.urls import path
from .views import AddNewsApiView

urlpatterns = [

    path('add_news/', AddNewsApiView.as_view(), name='add_news'),
]