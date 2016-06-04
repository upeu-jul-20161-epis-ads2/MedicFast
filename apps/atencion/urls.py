
from django.conf.urls import url

from .views import (PersonaListView, PersonaCreateView, PersonaUpdateView, PersonaDeleteView, ProductoListView, ProductoCreateView, ProductoDeleteView, ProductoUpdateView)

from .views import HitoriaBusquedaTemplateView

urlpatterns = [

<<<<<<< HEAD
    # distrito
    #url(r'^distrito/lista$', DistritoListView.as_view(), name="distrito_list"),
    #url(r'^distrito/detalle/(?P<pk>\d+)$', DistritoDetailView.as_view(), name="distrito_detail"),
    #url(r'^distrito/crear/$', DistritoCreateView.as_view(), name="distrito_add"),
    #url(r'^distrito/eliminar/(?P<pk>\d+)$', DistritoDeleteView.as_view(), name="distrito_delete"),
    #url(r'^distrito/editar/(?P<pk>\d+)$', DistritoUpdateView.as_view(), name="distrito_update"),

    url(r'^historial/busqueda$', HitoriaBusquedaTemplateView.as_view(), name="historia_busqueda"),

=======
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
>>>>>>> 9ee0fe2161baf4f24f7cf1924cbda8b41f77c0b2
]
