from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse,QueryDict
from django.shortcuts import render, redirect, reverse
from django.views import View, generic
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import SignUpSerializer, LoginSerializer, ProfileSerializer
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import permissions, renderers
from .models import CustomUser
from rest_framework_jwt.settings import api_settings
import json, datetime
import requests
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from news_categories.serializers import NewsCategoriesSerializer
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from news_categories.models import NewCategoriesModel


def date_date():
    date = datetime.datetime.now()
    return date.strftime('%A'), date.strftime('%d %b %Y')


class IndexApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        day, date = date_date()
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        return Response({'news':newsserializer.data,'date': date, 'day': day}, template_name='base.html')


class SignUpApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/registration.html'
    # style = {'template_pack': 'rest_framework/horizontal/'}
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        day, date = date_date()
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        serializer = SignUpSerializer()
        return Response({'news':newsserializer.data,'serializer': serializer, 'date': date, 'day': day})

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('index')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/login.html'
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()

    def get(self, request, format=None):
        serializer = LoginSerializer()
        day, date = date_date()
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        return Response({'news':newsserializer.data,'serializer': serializer, 'date': date, 'day': day})

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            data = json.dumps({'email': email, 'password': password})
            headers = {'content-type': 'application/json'}
            response_login = requests.post('http://127.0.0.1:8000/api-token-auth/',
                                           data=data, headers=headers)
            response_login_dict = json.loads(response_login.content)
            response_login_dict['status'] = 'success'
            return JsonResponse(response_login_dict, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'fail'})


class ProfileApiView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)

    def get(self, request, *args, **kwargs):
        day, date = date_date()
        user = self.get_object()
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        serializer = self.get_serializer(user)
        return Response({'news':newsserializer.data,'profile': serializer.data, 'date': date, 'day': day},
                        template_name='users/profile_detail.html')


class ProfileDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)

    def retrieve(self, request,  *args, **kwargs):
        day, date = date_date()
        user = self.get_object()
        news_categories = NewCategoriesModel.objects.all()
        newsserializer = NewsCategoriesSerializer(news_categories, many=True)
        serializer = self.get_serializer(user)
        return Response({'news':newsserializer.data,'profile': serializer.data, 'date': date, 'day': day},
                        template_name='users/profile_update.html')

    def put(self, request, *args, **kwargs):
        day, date = date_date()
        user = self.get_object()
        serializer = self.get_serializer(user,data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse({'status': 'success'})

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return JsonResponse({'status':'success'})