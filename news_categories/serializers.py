from rest_framework import serializers
from .models import NewCategoriesModel


class NewsCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewCategoriesModel
        fields = '__all__'


