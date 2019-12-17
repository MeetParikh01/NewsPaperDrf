from rest_framework import serializers
from .models import NewCategoriesModel, AddNewsModel
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe


class NewsCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewCategoriesModel
        fields = '__all__'


class AddNewsSerializer(serializers.ModelSerializer):
    Title = serializers.CharField(max_length=200, source='news_title')
    # Body = serializers.CharField(style={'base_template': 'textarea.html'},
    #                              source='news_body')
    # news_body = serializers.CharField(style={'template': 'widget.html'})
    #  news_body = serializers.SerializerMethodField()
    # category = serializers.RelatedField(source='news_category')


    # def get_news_body(self, instance):
    #     from django.utils.safestring import mark_safe
    #     return mark_safe(instance.news_body)

    class Meta:
        model = AddNewsModel
        fields = ('Title', 'image', 'news_body', 'news_category')


class Add(serializers.ModelSerializer):

    # news_body = serializers.ModelField(model_field=AddNewsModel()._meta.get_field('news_body'))
    news_body = serializers.CharField(style={'template': 'ckeditor.html'})
    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = AddNewsModel
        fields = ('news_title', 'image', 'news_body', 'news_category', 'thumbnail')

    # def validate_thumbnail(self, thumbnail):
    #     print('serializer called')
    #     print('+++++++++++++++++++++++', thumbnail)


