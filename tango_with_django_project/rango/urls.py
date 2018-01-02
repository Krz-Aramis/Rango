from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'about', views.about, name='about'),
    re_path(r'^rango', views.index, name='index'),
]
