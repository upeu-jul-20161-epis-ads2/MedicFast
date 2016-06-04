
from django.conf.urls import url

from .views import (DistritoListView, DistritoCreateView, DistritoUpdateView, DistritoDeleteView)

urlpatterns = [

    # distrito
    url(r'^distrito/lista$', DistritoListView.as_view(), name="distrito_list"),
    #url(r'^distrito/detalle/(?P<pk>\d+)$', DistritoDetailView.as_view(), name="distrito_detail"),
    url(r'^distrito/crear/$', DistritoCreateView.as_view(), name="distrito_add"),
    url(r'^distrito/eliminar/(?P<pk>\d+)$', DistritoDeleteView.as_view(), name="distrito_delete"),
    url(r'^distrito/editar/(?P<pk>\d+)$', DistritoUpdateView.as_view(), name="distrito_update"),
]
