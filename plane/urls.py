"""plane URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.static import serve

from plane import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^", include('planeapp.urls')),
    url(r'^media/(.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^doc/(.*)$', serve, {'document_root': settings.DOC_ROOT}),
    url(r'^login/$', LoginView.as_view(), name='login' ),
    # url(r'^media/(.*)$', logout, name='logout'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

]
