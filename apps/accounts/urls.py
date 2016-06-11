from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import LoginView, LogOutView, SignUpView, index, load_access, \
    EnterpriseAssociationCreateView
from django.contrib.auth import views as auth_views


accounts_patterns = [
    url(r'^', index, name='index'),
]

urlpatterns = [
    # Examples:
    # url(r'^$', 'plateo.views.home', name='home'),
    url(r'^load_access/(?P<headquar_id>.*)/(?P<module_id>.*)/$',
        load_access, name='load_access'),
    url(r'^add_enterprise/$',
        EnterpriseAssociationCreateView.as_view(), name='add_enterprise'),
    url(r'^$', include(accounts_patterns, namespace='accounts')),

    url(r'^login/$', LoginView.as_view(), name='login'),
    # url(r'^logout/$', auth_views.logout,
    #    {'template_name': 'registration/logged_out.html'}, name='logout'),

    url(r'^logout/$', LogOutView.as_view(), name='logout'),

    url(r'^register/', SignUpView.as_view(), name='register'),

    url(r'^password_reset/$',
        auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$',
        auth_views.password_reset_done, name='password_reset_done'),
    # Support old style base36 password reset links; remove in Django 1.7
    #url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    auth_views.password_reset_confirm_uidb36),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),


    url(r'^password/change/$', auth_views.password_change,
        name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done,
        name='password_change_done'),


]
