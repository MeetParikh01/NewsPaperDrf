"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from ckeditor_uploader import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.users_urls')),
    path('', include('news_categories.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest-auth/', include('rest_auth.urls')),
    path('api-token-auth/', obtain_jwt_token, name='token'),
    path('api-token-refresh/', refresh_jwt_token),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload/', login_required(views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
    path('api-token-verify/', verify_jwt_token)
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {
    #         'document_root': settings.MEDIA_ROOT
    #     })]