from django.urls import path
from .views import AddNewsApiView, NewsDisplay, \
    NewsDetailApiView, NewsCategoryApiView, NewsPostedByUserApiView, \
    NewsEditOrDeletePostedByUserApiView, DuplicateNewsPostedByUserApiView

urlpatterns = [

    path('add_news/', AddNewsApiView.as_view(), name='add_news'),
    path('news/', NewsDisplay.as_view()),
    path('news_detail/<int:pk>', NewsDetailApiView.as_view(), name='news_detail'),
    path('news_category/<int:pk>', NewsCategoryApiView.as_view(), name='news_category'),
    path('news_postedby_user/', NewsPostedByUserApiView.as_view(), name='news_postedby_user'),
    path('duplicate_news_postedby_user/', DuplicateNewsPostedByUserApiView.as_view(), name='duplicate_news_postedby_user'),
    path('news_modify_byuser/<int:pk>', NewsEditOrDeletePostedByUserApiView.as_view(), name='news_modify_byuser')
]
