from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^about', views.about, name='about'),
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
        document_root=settings.STATIC_ROOT)