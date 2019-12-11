from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View, generic
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import SignUpSerializer, LoginSerializer, TokenSerializer
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import permissions, renderers
from .models import CustomUser
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
class Index(View):
    def get(self, request):
        return render(request, 'base.html')


class SignUpApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/registration.html'
    # style = {'template_pack': 'rest_framework/horizontal/'}
    parser_classes = (FormParser, JSONParser, MultiPartParser)
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        serializer = SignUpSerializer()
        return Response({'serializer': serializer})

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
        return Response({'serializer': serializer})

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            token = jwt_encode_handler(
                    jwt_payload_handler(user)
                )
            # print(token, '+++++++++')
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            # print(serializer.initial_data['token'])
            print(serializer.is_valid(), '+++')
            try:
                if serializer.is_valid():
                    # import code;
                    # code.interact(local=dict(globals(), **locals()))
                    print('============================')
                    print(serializer.data.get('token'))
                    return Response({'data': serializer.data.get('token')})
            except Exception as e:
                print(e)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
