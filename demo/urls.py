"""backengo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.home import views as home_views
from django import views as django_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^home/', include('apps.home.urls', namespace='home')),
    url(r'^$', home_views.index, name='index'),

    url(r'^space/', include('apps.space.urls', namespace='space')),
    url(r'^sad/', include('apps.sad.urls', namespace='sad')),

    url(r'^mod_backend/',
        include('apps.mod_backend.urls', namespace='mod_backend')),

    url(r'^menu/', include('apps.accounts.urls')),


    # http://stackoverflow.com/questions/19625102/django-javascript-translation-not-working
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/', django_views.i18n.javascript_catalog),

    # atencion

    
    url(r'^atencion/', include('apps.atencion.urls', namespace="atencion")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# https://docs.djangoproject.com/en/1.6/ref/views/
# https://docs.djangoproject.com/en/1.6/howto/static-files/
"""
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': settings.DEBUG
    }),
"""
