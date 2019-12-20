from django.db import models
from users.models import CustomUser
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.
class NewCategoriesModel(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class AddNewsModel(models.Model):
    news_title = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='images/', default='default.jpeg')
    # thumbnail = models.ImageField(upload_to='thumbnail/', default=None, null=True)
    image = models.ImageField(upload_to='images/', default='default.jpeg')
    thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(200, 200)],
                                      format='JPEG',
                                      options={'quality': 60})
    news_body = RichTextUploadingField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    news_category = models.ForeignKey(NewCategoriesModel,
                                      on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.news_title

    # manually resize image
    # def save(self, *args, **kwargs):
    #     super(AddNewsModel, self).save(*args, **kwargs)
    #     print('save called')
    #     img = Image.open(self.thumbnail.path)
    #     if img.height > 250 or img.width > 250:
    #         output_size = (250, 250)
    #         img.thumbnail(output_size)
    #         # print('+++++++++++', self.thumbnail.path)
    #         img.save(self.thumbnail.path)



