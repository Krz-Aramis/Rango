"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.views.static import serve
from rango import views

from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, new_user):
        return '/rango/register_profile'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rango.urls')),
    path('accounts/register/', MyRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
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
