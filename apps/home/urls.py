from django.conf.urls import url
from django.views.generic import TemplateView
from apps.home import views as home_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'plateo.views.home', name='home'),
    url(r'^saludo_hola/(?P<nombre>\w+)/',
        home_views.saludo_hola_view, name='saludo-hola'),

    url(r'^saludo_hola_template/(?P<nombre>\w+)/',
        home_views.saludo_hola_template_view,
        name='saludo-hola-template'),

    # url(r'^$', TemplateView.as_view(template_name='home/base_home.html')),

    url(r'^', home_views.index, name='index'),
    url(r'^index/', home_views.index, name='index'),


]
