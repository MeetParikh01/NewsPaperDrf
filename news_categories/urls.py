from django.urls import path
from .views import AddNewsApiView, NewsDisplay

urlpatterns = [

    path('add_news/', AddNewsApiView.as_view(), name='add_news'),
    path('news/', NewsDisplay.as_view())
]