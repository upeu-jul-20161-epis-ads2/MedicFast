# _*_ coding: utf-8 _*_
from django.conf.urls import url

# views
from .views import HeadquarListView, HeadquarUpdateView, HeadquarCreateView, \
    HeadquarUpdateActiveView, HeadquarAssociationUpdateView

from .views import EnterpriseUpdateView, EnterpriseListView, \
    EnterpriseCreateView, EnterpriseDeleteView, EnterpriseUpdateActiveView
from .views import AssociationUpdateView
from .views import SolutionListView, SolutionCreateView,\
    SolutionUpdateView, SolutionDeleteView, SolutionUpdateActiveView

# public
urlpatterns = [
    url(r'^headquar/update_association/(?P<pk>.*)/$',
        HeadquarAssociationUpdateView.as_view(), name='headquar-update_association'),
    url(r'^headquar/state/(?P<state>[\w\d\-]+)/(?P<pk>.*)/$',
        HeadquarUpdateActiveView.as_view(), name='headquar-state'),
    url(r'^headquar/create/$',
        HeadquarCreateView.as_view(), name='headquar-create'),
    url(r'^headquar/update/(?P<pk>.*)/$',
        HeadquarUpdateView.as_view(), name='headquar-update'),
    url(r'^headquar/index/$',
        HeadquarListView.as_view(), name='headquar-list'),

    # enterprise x asullom
    url(r'^enterprise/state/(?P<state>[\w\d\-]+)/(?P<pk>.*)/$',
        EnterpriseUpdateActiveView.as_view(), name='enterprise-state'),
    url(r'^enterprise/delete/(?P<pk>.*)/$',
        EnterpriseDeleteView.as_view(), name='enterprise-delete'),
    url(r'^enterprise/create/$',
        EnterpriseCreateView.as_view(), name='enterprise-create'),
    url(r'^enterprise/update/(?P<pk>.*)/$',
        EnterpriseUpdateView.as_view(), name='enterprise-update'),
    url(r'^enterprise/index/$',
        EnterpriseListView.as_view(), name='enterprise-list'),
    url(r'^enterprise/edit_current/$',
        EnterpriseUpdateView.as_view(), name='enterprise-edit_current'),


    url(r'^association/edit_current/$',
        AssociationUpdateView.as_view(), name='association-edit_current'),

    # solution x asullom
    url(r'^solution/state/(?P<state>[\w\d\-]+)/(?P<pk>.*)/$',
        SolutionUpdateActiveView.as_view(), name='solution-state'),
    url(r'^solution/delete/(?P<pk>.*)/$',
        SolutionDeleteView.as_view(), name='solution-delete'),
    url(r'^solution/update/(?P<pk>.*)/$',
        SolutionUpdateView.as_view(), name='solution-update'),
    url(r'^solution/create/$',
        SolutionCreateView.as_view(), name='solution-create'),
    url(r'^solution/index/$',
        SolutionListView.as_view(), name='solution-list'),

]