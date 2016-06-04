
from django.conf.urls import url

from .views import (PersonaListView, PersonaCreateView, PersonaUpdateView, PersonaDeleteView, ProductoListView, ProductoCreateView, ProductoDeleteView, ProductoUpdateView)

urlpatterns = [

    # persona
    url(r'^persona/lista$', PersonaListView.as_view(), name="persona_list"),
    url(r'^persona/crear/$', PersonaCreateView.as_view(), name="persona_add"),
    url(r'^persona/eliminar/(?P<pk>\d+)$', PersonaDeleteView.as_view(), name="persona_delete"),
    url(r'^persona/editar/(?P<pk>\d+)$', PersonaUpdateView.as_view(), name="persona_update"),

    #Producto
    url(r'^producto/lista$', ProductoListView.as_view(), name="producto_list"),
    url(r'^producto/crear/$', ProductoCreateView.as_view(), name="producto_add"),
    url(r'^producto/eliminar/(?P<pk>\d+)$', ProductoDeleteView.as_view(), name="producto_delete"),
    url(r'^producto/editar/(?P<pk>\d+)$', ProductoUpdateView.as_view(), name="producto_update"),
]
