from django.urls import path
from .views import AddNewsApiView, NewsDisplay, NewsDetailApiView, NewsCategoryApiView

urlpatterns = [

    path('add_news/', AddNewsApiView.as_view(), name='add_news'),
    path('news/', NewsDisplay.as_view()),
    path('news_detail/<int:pk>', NewsDetailApiView.as_view(), name='news_detail'),
    path('news_category/<int:pk>', NewsCategoryApiView.as_view(), name='news_category'),

]
