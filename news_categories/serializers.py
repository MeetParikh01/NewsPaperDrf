from rest_framework import serializers
from . import models
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
        fields = ('news_title', 'image', 'news_body', 'news_category', 'thumbnail', 'date')

    # def validate_thumbnail(self, thumbnail):
    #     print('serializer called')
    #     print('+++++++++++++++++++++++', thumbnail)


class NewsGroupbyCategorySerializer(serializers.Serializer):
    Mobile = serializers.SerializerMethodField()
    Tablet = serializers.SerializerMethodField()
    Gadgets = serializers.SerializerMethodField()
    Camera = serializers.SerializerMethodField()
    Laptop_PC = serializers.SerializerMethodField()

    class Meta:
        model = AddNewsModel
        fields = ('mobile', 'tablet', 'gadgets', 'camera', 'laptop')

    def query(self, category_name):
        category = NewCategoriesModel.objects.get(category_name=category_name)
        return AddNewsModel.objects.\
            filter(news_category=category)

    def get_Mobile(self, instance):
        return [{'id': i.id, 'news_title': i.news_title, 'author':i.user.first_name+' '+i.user.last_name,
                 'date':str(i.date.strftime('%d%b-%Y')), 'image':i.image.url, 'thumbnail':i.thumbnail.url,
                 'news_body':i.news_body, 'news_category':i.news_category.id} for i in self.query('Mobile')]
        # return Add(self.query('Mobile')
        #            , many=True).data

    def get_Tablet(self, instance):
        return [{'id': i.id, 'news_title': i.news_title, 'author': i.user.first_name + ' ' + i.user.last_name,
                 'date': str(i.date.strftime('%d%b-%Y')), 'image': i.image.url, 'thumbnail': i.thumbnail.url,
                 'news_body': i.news_body, 'news_category': i.news_category.id} for i in self.query('Tablet')]
        # return Add(self.query('Tablet')
        #            , many=True).data

    def get_Gadgets(self, instance):
        return [{'id': i.id, 'news_title': i.news_title, 'author': i.user.first_name + ' ' + i.user.last_name,
                 'date': str(i.date.strftime('%d%b-%Y')), 'image': i.image.url, 'thumbnail': i.thumbnail.url,
                 'news_body': i.news_body, 'news_category': i.news_category.id} for i in self.query('Gadgets')]
        # return Add(self.query('Gadgets')
        #            , many=True).data

    def get_Camera(self, instance):
        return [{'id': i.id, 'news_title': i.news_title, 'author': i.user.first_name + ' ' + i.user.last_name,
                 'date': str(i.date.strftime('%d%b-%Y')), 'image': i.image.url, 'thumbnail': i.thumbnail.url,
                 'news_body': i.news_body, 'news_category': i.news_category.id} for i in self.query('Camera')]
        # return Add(self.query('Camera')
        #            , many=True).data

    def get_Laptop_PC(self, instance):
        return [{'id': i.id, 'news_title': i.news_title, 'author': i.user.first_name + ' ' + i.user.last_name,
                 'date': str(i.date.strftime('%d%b-%Y')), 'image': i.image.url, 'thumbnail': i.thumbnail.url,
                 'news_body': i.news_body, 'news_category': i.news_category.id} for i in self.query('Laptop/ PC')]
        # return Add(self.query('Laptop/ PC')
        #            , many=True).data


class NewsDetailOrByCategorySerializer(serializers.ModelSerializer):

    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = AddNewsModel
        fields = ('id', 'user', 'news_category', 'date', 'thumbnail', 'news_title', 'news_body', 'image')

    def to_representation(self, instance):
        data = super(NewsDetailOrByCategorySerializer, self).to_representation(instance)
        data.update({'user': instance.user.first_name+' '+instance.user.last_name,
                        'news_category':instance.news_category.category_name})
        return data


class NewsModifySerializer(serializers.ModelSerializer):
    # thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = AddNewsModel
        fields = ('id',  'news_category',   'news_title', 'news_body', 'image')

# class NewsListSerializer(serializers.ListSerializer):
#
#     def to_representation(self, data):
#         iterable = data.all() if isinstance(data, models.Manager) else data
#
#         return {category: super().to_representation(AddNewsModel.objects.filter(news_category=category))
#                   for category in NewCategoriesModel.objects.all()}
#
#
# class News(serializers.Serializer):
#
#     class Meta:
#         list_serializer_class = NewsListSerializer

