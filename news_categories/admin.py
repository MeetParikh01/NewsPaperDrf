from django.contrib import admin
from .models import NewCategoriesModel, AddNewsModel

# Register your models here.
admin.site.register(NewCategoriesModel)
admin.site.register(AddNewsModel)