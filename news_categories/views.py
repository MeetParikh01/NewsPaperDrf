import datetime
from django.shortcuts import render, redirect
from rest_framework import status, permissions, renderers
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from .models import NewCategoriesModel, AddNewsModel
from .serializers import AddNewsSerializer, NewsCategoriesSerializer, Add


def date_date():
    date = datetime.datetime.now()
    return date.strftime('%A'), date.strftime('%d %b %Y')


# Create your views here.
class AddNewsApiView(ListCreateAPIView):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    parser_classes = (FormParser, JSONParser, MultiPartParser)
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
