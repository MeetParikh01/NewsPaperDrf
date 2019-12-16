from django.db import models


# Create your models here.
class NewCategoriesModel(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name
