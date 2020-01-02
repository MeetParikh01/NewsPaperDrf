import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status, permissions, renderers
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import NewCategoriesModel, AddNewsModel
from .serializers import AddNewsSerializer, NewsCategoriesSerializer,\
    Add, NewsGroupbyCategorySerializer,  NewsDetailOrByCategorySerializer, NewsModifySerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


def date_date():
    date = datetime.datetime.now()
    return date.strftime('%A'), date.strftime('%d %b %Y')


# Create your views here.
class AddNewsApiView(ListCreateAPIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    queryset = AddNewsModel.objects.all()
    serializer_class = Add

    def list(self, request, *args, **kwargs):
        day, date = date_date()
        serializer = self.get_serializer()
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        return Response({'news':newsserializer.data, 'date':date, 'day':day, 'serializer': serializer},
                        template_name='news_categories/news_post.html')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            # serializer.save(user=self.request.user, thumbnail=request.data.get('image'))
            return redirect('index')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class NewsDisplay(APIView):
    # renderer_classes = [renderers.TemplateHTMLRenderer]
    # parser_classes = (FormParser, JSONParser, MultiPartParser)
    permission_classes = [permissions.AllowAny]
    # authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request, *args, **kwargs):
        data= AddNewsModel.objects.all()
        serializer = NewsGroupbyCategorySerializer(data)
        return Response(serializer.data)


class NewsDetailApiView(RetrieveAPIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    queryset = AddNewsModel.objects.all()
    serializer_class = NewsDetailOrByCategorySerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        day, date = date_date()
        news_detail = self.get_object()
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        serializer = self.get_serializer(news_detail)
        return Response({'news':newsserializer.data, 'news_detail': serializer.data, 'date': date, 'day': day},
                        template_name='news_categories/news_detail.html')


class NewsCategoryApiView(RetrieveAPIView):
    serializer_class = NewsDetailOrByCategorySerializer
    renderer_classes = [renderers.TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        day, date = date_date()
        news_category = AddNewsModel.objects.filter(news_category=kwargs.get('pk'))\
            .order_by('id')
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        serializer = self.get_serializer(news_category, many=True)
        category_name = serializer.data[0].get('news_category')
        return Response({'news': newsserializer.data,'category':category_name, 'news_category': serializer.data, 'date': date, 'day': day},
                        template_name='news_categories/news_by_category.html')


class NewsPostedByUserApiView(RetrieveAPIView):
    serializer_class = NewsDetailOrByCategorySerializer
    renderer_classes = [renderers.TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)

    def get(self, request, *args, **kwargs):
        day, date = date_date()
        news_category = AddNewsModel.objects.filter(user=request.user) \
            .order_by('id')
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        serializer = self.get_serializer(news_category, many=True)
        return Response(
            {'news': newsserializer.data, 'news_category': serializer.data, 'date': date,
             'day': day}, template_name='news_categories/news_postedby_user.html')


class NewsEditOrDeletePostedByUserApiView(RetrieveUpdateDestroyAPIView):
    queryset = AddNewsModel.objects.all()
    serializer_class = NewsModifySerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)

    def retrieve(self, request,  *args, **kwargs):
        day, date = date_date()
        news = self.get_object()
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        serializer = self.get_serializer(news)
        return Response({'news':newsserializer.data, 'post': serializer.data, 'date': date, 'day': day},
                        template_name='news_categories/news_post_update.html')

    def put(self, request, *args, **kwargs):
        news = self.get_object()
        data = request.data
        serializer = self.get_serializer(news, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse({'status': 'success'})

    def destroy(self, request, *args, **kwargs):
        news = self.get_object()
        news.delete()
        return JsonResponse({'status':'success'})


class DuplicateNewsPostedByUserApiView(RetrieveAPIView):
    serializer_class = NewsDetailOrByCategorySerializer
    renderer_classes = [renderers.TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request, *args, **kwargs):
        print(request.headers)
        day, date = date_date()
        news_category = AddNewsModel.objects.filter(user=request.user) \
            .order_by('id')
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        serializer = self.get_serializer(news_category, many=True)
        return Response(
            {'news': newsserializer.data, 'news_category': serializer.data, 'date': date,
             'day': day}, template_name='news_categories/news_postedby_user.html')
