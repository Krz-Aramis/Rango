from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^about', views.about, name='about'),
]

# TODO: remove this BEFORE deployment. It is not efficient or recommended.
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
        document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [ re_path(r'^media/(?P<path>.*)$', 
                       serve, 
                       {'document_root': settings.MEDIA_ROOT,})
    ]