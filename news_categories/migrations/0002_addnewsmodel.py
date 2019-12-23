# Generated by Django 2.2 on 2019-12-16 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddNewsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=200)),
                ('image', models.ImageField(default='default.jpeg', upload_to='images/')),
                ('news_body', models.TextField()),
                ('news_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news_categories.NewCategoriesModel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]