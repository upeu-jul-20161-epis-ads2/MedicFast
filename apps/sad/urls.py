# _*_ coding: utf-8 _*_
from django.conf.urls import url  # , include

# views
from .views import UserListView, UserCreateView, UserUpdateView, \
    UserDeleteView, UserActiveUpdateView, PersonListView

from .views import MenuListView, MenuCreateView, MenuUpdateView, \
    MenuDeleteView, MenuUpdateActiveView, UserDetailView

from .views import ModuleListView, ModuleCreateView, \
    ModuleUpdateView, ModuleDeleteView, ModuleUpdateActiveView, \
    ModuleSolutionsUpdateView

from .views import GroupListView, GroupCreateView, GroupUpdateView,\
    GroupDeleteView, GroupPermissionsUpdateView

from .views import PermissionListView, PermissionCreateView, \
    PermissionUpdateView, PermissionDeleteView

# public
urlpatterns = [
    # user x asullom
     url(r'^user/person_add/(?P<pk>.*)/$',
        UserCreateView.as_view(), name='user-person_add'),
    url(r'^user/person_search/$',
        PersonListView.as_view(), name='user-person_search'),
    url(r'^user/detail/(?P<pk>.*)/$',
        UserDetailView.as_view(), name='user-detail'),
    url(r'^user/state/(?P<state>[\w\d\-]+)/(?P<pk>.*)/$',
        UserActiveUpdateView.as_view(), name='user-state'),
    url(r'^user/delete/(?P<pk>.*)/$',
        UserDeleteView.as_view(), name='user-delete'),
    url(r'^user/update/(?P<pk>.*)/$',
        UserUpdateView.as_view(), name='user-update'),
    url(r'^user/create/$',
        UserCreateView.as_view(), name='user-create'),
    url(r'^user/index/$',
        UserListView.as_view(), name='user-list'),

    # menu x asullom
    url(r'^menu/state/(?P<state>[\w\d\-]+)/(?P<pk>.*)/$',
        MenuUpdateActiveView.as_view(), name='menu-state'),
    url(r'^menu/delete/(?P<pk>.*)/$',
        MenuDeleteView.as_view(), name='menu-delete'),
    url(r'^menu/update/(?P<pk>.*)/$',
        MenuUpdateView.as_view(), name='menu-update'),
    url(r'^menu/create/$',
        MenuCreateView.as_view(), name='menu-create'),
    url(r'^menu/index/$',
        MenuListView.as_view(), name='menu-list'),

    # module x asullom
    url(r'^modulesolutions/update/$',  # modulesolutions es el controller
        ModuleSolutionsUpdateView.as_view(), name='modulesolutions-update'),
    url(r'^module/state/(?P<state>[\w\d\-]+)/(?P<pk>.*)/$',
        ModuleUpdateActiveView.as_view(), name='module-state'),
    url(r'^module/delete/(?P<pk>.*)/$',
        ModuleDeleteView.as_view(), name='module-delete'),
    url(r'^module/update/(?P<pk>.*)/$',
        ModuleUpdateView.as_view(), name='module-update'),
    url(r'^module/create/$',
        ModuleCreateView.as_view(), name='module-create'),
    url(r'^module/index/$',
        ModuleListView.as_view(), name='module-list'),

    # group x asullom
    url(r'^grouppermissions/update/$',  # grouppermissions es el controller
        GroupPermissionsUpdateView.as_view(), name='grouppermissions-update'),
    url(r'^group/delete/(?P<pk>.*)/$',
        GroupDeleteView.as_view(), name='group-delete'),
    url(r'^group/update/(?P<pk>.*)/$',
        GroupUpdateView.as_view(), name='group-update'),
    url(r'^group/create/$',
        GroupCreateView.as_view(), name='group-create'),
    url(r'^group/index/$',
        GroupListView.as_view(), name='group-list'),

    # permission x asullom
    url(r'^permission/delete/(?P<pk>.*)/$',
        PermissionDeleteView.as_view(), name='permission-delete'),  # x pony
    url(r'^permission/update/(?P<pk>.*)/$',
        PermissionUpdateView.as_view(), name='permission-update'),
    url(r'^permission/create/$',
        PermissionCreateView.as_view(), name='permission-create'),
    url(r'^permission/index/$',
        PermissionListView.as_view(), name='permission-list'),
    # url(r'^permission/', include(permission_patterns)),
]


permission_patterns = [
    url(r'^index/$',
        PermissionListView.as_view(), name='permission-list'),

    url(r'^create/$',
        PermissionCreateView.as_view(), name='permission-create'),

    url(r'^update/(?P<pk>.*)/$',
        PermissionUpdateView.as_view(), name='permission-update'),

    url(r'^delete/(?P<pk>.*)/$',
        PermissionDeleteView.as_view(), name='permission-delete'),

]
