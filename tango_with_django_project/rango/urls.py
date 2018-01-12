from django.urls import path, re_path
from django.conf.urls import url
from . import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^rango/$', views.index, name='index'),
    re_path(r'category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    re_path(r'about', views.about, name='about'),
    re_path(r'^add_category/$', views.add_category, name='add_category'),
    re_path(r'category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    re_path(r'restricted/$', views.restricted, name='restricted'),
    re_path(r'goto/', views.track_url, name='goto'),
    re_path(r'register_profile/$', views.register_profile, name='register_profile')
]
