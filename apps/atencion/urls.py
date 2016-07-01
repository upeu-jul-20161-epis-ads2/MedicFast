
from django.conf.urls import url
from django.conf.urls import patterns, include, url
from apps.atencion.views import DiagnosticoBuscar
from .views import PersonaListView, PersonaCreateView, PersonaUpdateView, PersonaDeleteView
from .views import ProductoListView, ProductoCreateView, ProductoDeleteView, ProductoUpdateView
from .views import LaboratorioListView, LaboratorioCreateView, LaboratorioDeleteView, LaboratorioUpdateView
from .views import FuncionesVitalesListView, FuncionesVitalesCreateView, FuncionesVitalesDeleteView, FuncionesVitalesUpdateView
from .views import PeriodoListView, PeriodoCreateView, PeriodoDeleteView, PeriodoUpdateView
from .views import DiagnosticoListView, DiagnosticoDeleteView, DiagnosticoUpdateView, DiagnosticoCreateView, DiagnosticoConsultaCreate
from .views import UnidadMedidaCreateView, UnidadMedidaListView, UnidadMedidaUpdateView, UnidadMedidaDeleteView
from .views import (PersonaListView, PersonaCreateView, PersonaUpdateView, PersonaDeleteView, ProductoListView, ProductoCreateView, ProductoDeleteView, ProductoUpdateView,
    ProvinciaAjax, DistritoAjax, HitoriaDetailView, AntecedenteCreateView, DiagnosticoConsultaCreate, ProductoBuscarAjaxView)
from .views import HitoriaBusquedaTemplateView, HitoriaCreateView, vista, BarView

urlpatterns = [

    url(r'^historia/busqueda$', HitoriaBusquedaTemplateView.as_view(), name="historia_search"),
    url(r'^historia/crear$', HitoriaCreateView.as_view(), name="historia_add"),
    url(r'^historia/detalle/(?P<pk>\d+)$', HitoriaDetailView.as_view(), name="historia_detail"),

    # persona
    url(r'^persona/lista$', PersonaListView.as_view(), name="persona_list"),
    url(r'^persona/crear/$', PersonaCreateView.as_view(), name="persona_add"),
    url(r'^persona/eliminar/(?P<pk>\d+)$', PersonaDeleteView.as_view(), name="persona_delete"),
    url(r'^persona/editar/(?P<pk>\d+)$', PersonaUpdateView.as_view(), name="persona_update"),
    url(r'^distrito_ajax/$', DistritoAjax.as_view(), name='busqueda_distrito'),
    url(r'^provincia_ajax/$', ProvinciaAjax.as_view(), name='busqueda_provincia'),

    # Producto
    url(r'^producto/lista$', ProductoListView.as_view(), name="producto_list"),
    url(r'^producto/crear/$', ProductoCreateView.as_view(), name="producto_add"),
    url(r'^producto/eliminar/(?P<pk>\d+)$', ProductoDeleteView.as_view(), name="producto_delete"),
    url(r'^producto/editar/(?P<pk>\d+)$', ProductoUpdateView.as_view(), name="producto_update"),
    url(r'^producto/buscar/$', ProductoBuscarAjaxView.as_view(), name="medicamento_search"),
    # Laboratorio
    url(r'^laboratorio/lista$', LaboratorioListView.as_view(), name="laboratorio_list"),
    url(r'^laboratorio/crear/$', LaboratorioCreateView.as_view(), name="laboratorio_add"),
    url(r'^laboratorio/eliminar/(?P<pk>\d+)$', LaboratorioDeleteView.as_view(), name="laboratorio_delete"),
    url(r'^laboratorio/editar/(?P<pk>\d+)$', LaboratorioUpdateView.as_view(), name="laboratorio_update"),


    # FuncionesVitales
    url(r'^funcionesvitales/lista$', FuncionesVitalesListView.as_view(), name="funcionesvitales_list"),
    url(r'^funcionesvitales/crear/$', FuncionesVitalesCreateView.as_view(), name="funcionesvitales_add"),
    url(r'^funcionesvitales/eliminar/(?P<pk>\d+)$', FuncionesVitalesDeleteView.as_view(), name="funcionesvitales_delete"),
    url(r'^funcionesvitales/editar/(?P<pk>\d+)$', FuncionesVitalesUpdateView.as_view(), name="funcionesvitales_update"),

    # Periodo
    url(r'^periodo/lista$', PeriodoListView.as_view(), name="periodo_list"),
    url(r'^periodo/crear/$', PeriodoCreateView.as_view(), name="periodo_add"),
    url(r'^periodo/eliminar/(?P<pk>\d+)$', PeriodoDeleteView.as_view(), name="periodo_delete"),
    url(r'^periodo/editar/(?P<pk>\d+)$', PeriodoUpdateView.as_view(), name="periodo_update"),

    # Diagnostico
    url(r'^diagnostico/lista$', DiagnosticoListView.as_view(), name="diagnostico_list"),
    url(r'^diagnostico/crear/$', DiagnosticoConsultaCreate.as_view(), name="diagnostico_add"),
    url(r'^diagnostico/nuevo/$', DiagnosticoCreateView.as_view(), name="diagnostico_create"),
    url(r'^diagnostico/eliminar/(?P<pk>\d+)$', DiagnosticoDeleteView.as_view(), name="diagnostico_delete"),
    url(r'^diagnostico/editar/(?P<pk>\d+)$', DiagnosticoUpdateView.as_view(), name="diagnostico_update"),
    url(r'^diagnostico/buscarajax$', DiagnosticoBuscar.as_view(), name="diagnostico_search"),

    # UnidadMedida
    url(r'^unidadmedida/lista$', UnidadMedidaListView.as_view(), name="unidadmedida_list"),
    url(r'^unidadmedida/crear/$', UnidadMedidaCreateView.as_view(), name="unidadmedida_add"),
    url(r'^unidadmedida/eliminar/(?P<pk>\d+)$', UnidadMedidaDeleteView.as_view(), name="unidadmedida_delete"),
    url(r'^unidadmedida/editar/(?P<pk>\d+)$', UnidadMedidaUpdateView.as_view(), name="unidadmedida_update"),

    # Antecedentes
    url(r'^antecedente/crear/$', AntecedenteCreateView.as_view(), name="antecedente_add"),

    #Reportes
    url(r'^reporte/atencion/$', vista, name="reporte_atencion"),
    url(r'^barbash/$', BarView.as_view(), name="bar"),

   



]
