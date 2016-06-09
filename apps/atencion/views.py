import logging
log = logging.getLogger(__name__)
from apps.utils.security import SecurityKey, log_params, UserToken, get_dep_objects
from django import http
from django.conf.locale import da
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.core import serializers
from django.http import HttpResponse, request
from django.db.models import Max, Sum
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404
from datetime import datetime, time, date
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.utils.encoding import force_text
from django.contrib.messages.views import SuccessMessageMixin
from apps.utils.decorators import permission_resource_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _ 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from apps.utils.forms import empty
import json
from django.utils.text import capfirst, get_text_list
from .forms.PersonaForm import PersonaForm
from .forms.LaboratorioForm import LaboratorioForm
from .forms.ProductoForm import ProductoForm
from .forms.PeriodoForm import PeriodoForm
from .forms.FuncionesVitalesForm import FuncionesVitalesForm
from .forms.UnidadMedidaForm import UnidadMedidaForm
from .forms.DiagnosticoForm import DiagnosticoForm
from .models import (Persona, Producto, Laboratorio, FuncionesVitales, Periodo, Diagnostico,UnidadMedida)


# class Persona==============================================================================
class PersonaListView(ListView):
    model = Persona
    template_name = 'persona/persona_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PersonaListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'nombres')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(PersonaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'persona'
        context['title'] = _('Select %s to change') % capfirst(_('Persona'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class ProvinciaAjax(TemplateView):
    """docstring for BusquedaAjaxView"""
    def get(self, request, *args, **kwargs):
        options = '<option value="" selected="selected">---------</option>'

        id_departamento = request.GET.get('id')
        if id_departamento:

            provincias = Provincia.objects.filter(departamento__id=id_departamento)

        else:
            provincias = Provincia.objects.filter(departamento__id=0)
        # data = serializers.serialize('json', distritos, fields=('id', 'distrito'))
        for provincia in provincias:
            options += '<option value="%s">%s</option>' % (
                provincia.pk,
                provincia.nombre
            )
        response = {}
        response['provincias'] = options

        return http.JsonResponse(response)

class DistritoAjax(TemplateView):
    """docstring for BusquedaAjaxView"""
    def get(self, request, *args, **kwargs):

        options = '<option value="" selected="selected">---------</option>'

        id_provincia = request.GET.get('id')
        if id_provincia:

            distritos = Distrito.objects.filter(provincia__id=id_provincia)
            
        else:
            distritos = Distrito.objects.filter(provincia__id=0)
        # data = serializers.serialize('json', distritos, fields=('id', 'distrito'))
        for distrito in distritos:
            options += '<option value="%s">%s</option>' % (
                distrito.pk,
                distrito.nombre
            )
        response = {}
        response['distritos'] = options

        return http.JsonResponse(response)


class PersonaCreateView(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/persona_add.html'
    success_url = reverse_lazy('atencion:persona_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(PersonaCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonaCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'persona'
        context['title'] = ('Agregar %s') % ('Persona')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        self.object.usuario = self.request.user

        
        msg = (' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(PersonaCreateView, self).form_valid(form)



class PersonaUpdateView(UpdateView):
    model = Persona
    template_name = 'persona/persona_add.html'
    form_class = PersonaForm
    success_url = reverse_lazy('atencion:persona_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(PersonaUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonaUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'persona'
        context['title'] = _('Add %s') % _('Persona')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(PersonaUpdateView, self).form_valid(form)


class PersonaDeleteView(DeleteView):
    model = Persona
    success_url = reverse_lazy('atencion:persona_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(PersonaDeleteView, self).dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request,  ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)


            d.delete()
            msg = _(' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class HitoriaBusquedaTemplateView(TemplateView):
    """Historia Template View.

    Clase usada para buscar el historial de una persona.
    """

    template_name = "historial/busqueda.html"

    def get(self, request, *args, **kwargs):
        try:
            codigo = request.GET['codigo']
            
            persona = Persona.objects.get(dni=codigo)


        except Exception as e:
            persona = ''

        try:
            historia = Historia.objects.get(persona__dni=codigo)

        except Exception as e:
            historia = ''

        context = {'persona': persona, 'historia': historia}


        return self.render_to_response(context)

# class Producto==============================================================================
class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/producto_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'codigo')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(ProductoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'producto'
        context['title'] = _('Select %s to change') % capfirst(_('Producto'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/producto_add.html'
    success_url = reverse_lazy('atencion:producto_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductoCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'producto'
        context['title'] = ('Agregar %s') % ('Producto')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        self.object.usuario = self.request.user

        
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(ProductoCreateView, self).form_valid(form)



class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'producto/producto_add.html'
    form_class = ProductoForm
    success_url = reverse_lazy('atencion:producto_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductoUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'producto'
        context['title'] = _('Add %s') % _('Producto')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(ProductoUpdateView, self).form_valid(form)


class ProductoDeleteView(DeleteView):
    model = Producto
    success_url = reverse_lazy('atencion:producto_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(ProductoDeleteView, self).dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request,  ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)


            d.delete()
            msg = _(' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# class Laboratorio==============================================================================
class LaboratorioListView(ListView):
    model = Laboratorio
    template_name = 'laboratorio/laboratorio_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LaboratorioListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'hemoglobina')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(LaboratorioListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'laboratorio'
        context['title'] = _('Select %s to change') % capfirst(_('Laboratorio'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class LaboratorioCreateView(CreateView):
    model = Laboratorio
    form_class = LaboratorioForm
    template_name = 'laboratorio/laboratorio_add.html'
    success_url = reverse_lazy('atencion:laboratorio_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(LaboratorioCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LaboratorioCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'laboratorio'
        context['title'] = ('Agregar %s') % ('Laboratorio')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        self.object.usuario = self.request.user

        
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(LaboratorioCreateView, self).form_valid(form)



class LaboratorioUpdateView(UpdateView):
    model = Laboratorio
    template_name = 'laboratorio/laboratorio_add.html'
    form_class = LaboratorioForm
    success_url = reverse_lazy('atencion:laboratorio_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(LaboratorioUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LaboratorioUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'laboratorio'
        context['title'] = _('Add %s') % _('Laboratorio')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(LaboratorioUpdateView, self).form_valid(form)


class LaboratorioDeleteView(DeleteView):
    model = Laboratorio
    success_url = reverse_lazy('atencion:laboratorio_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(LaboratorioDeleteView, self).dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request,  ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)


            d.delete()
            msg = _(' %(name)s "%(obj)s" fuel eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# class FuncionesVitales==============================================================================
class FuncionesVitalesListView(ListView):
    model = FuncionesVitales
    template_name = 'funciones_vitales/funcionesvitales_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FuncionesVitalesVitalesListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'peso')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(FuncionesVitalesListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'funcionesvitales'
        context['title'] = _('Select %s to change') % capfirst(_('FuncionesVitales'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class FuncionesVitalesCreateView(CreateView):
    model = FuncionesVitales
    form_class = FuncionesVitalesForm
    template_name = 'funciones_vitales/funcionesvitales_add.html'
    success_url = reverse_lazy('atencion:funcionesvitales_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(FuncionesVitalesCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FuncionesVitalesCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'funcionesvitales'
        context['title'] = ('Agregar %s') % ('FuncionesVitales')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        self.object.usuario = self.request.user

        
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(FuncionesVitalesCreateView, self).form_valid(form)



class FuncionesVitalesUpdateView(UpdateView):
    model = FuncionesVitales
    template_name = 'funciones_vitales/funcionesvitales_add.html'
    form_class = FuncionesVitalesForm
    success_url = reverse_lazy('atencion:funcionesvitales_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(FuncionesVitalesUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FuncionesVitalesUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'funcionesvitales'
        context['title'] = _('Add %s') % _('FuncionesVitales')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(FuncionesVitalesUpdateView, self).form_valid(form)


class FuncionesVitalesDeleteView(DeleteView):
    model = FuncionesVitales
    success_url = reverse_lazy('atencion:funcionesvitales_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(FuncionesVitalesDeleteView, self).dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request,  ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)


            d.delete()
            msg = _(' %(name)s "%(obj)s" fuel eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# class Periodo==============================================================================

class PeriodoListView(ListView):
    model = Periodo
    template_name = 'periodo/periodo_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PeriodoListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'ciclo')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(PeriodoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'periodo'
        context['title'] = _('Select %s to change') % capfirst(_('Periodo'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class PeriodoCreateView(CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'periodo/periodo_add.html'
    success_url = reverse_lazy('atencion:periodo_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(PeriodoCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PeriodoCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'periodo'
        context['title'] = ('Agregar %s') % ('Periodo')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        self.object.usuario = self.request.user

        
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(PeriodoCreateView, self).form_valid(form)



class PeriodoUpdateView(UpdateView):
    model = Periodo
    template_name = 'periodo/periodo_add.html'
    form_class = PeriodoForm
    success_url = reverse_lazy('atencion:periodo_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(PeriodoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PeriodoUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'periodo'
        context['title'] = _('Add %s') % _('Periodo')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(PeriodoUpdateView, self).form_valid(form)


class PeriodoDeleteView(DeleteView):
    model = Periodo
    success_url = reverse_lazy('atencion:periodo_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(PeriodoDeleteView, self).dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request,  ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)


            d.delete()
            msg = _(' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# class Diagnostico==============================================================================

class DiagnosticoListView(ListView):
    model = Diagnostico
    template_name = 'diagnostico/diagnostico_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DiagnosticoListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'codigo')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(DiagnosticoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'diagnostio'
        context['title'] = _('Select %s to change') % capfirst(_('Diagnostico'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class DiagnosticoCreateView(CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'diagnostico/diagnostico_add.html'
    success_url = reverse_lazy('atencion:diagnostico_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(DiagnosticoCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiagnosticoCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'diagnostico'
        context['title'] = ('Agregar %s') % ('Diagnostico')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        self.object.usuario = self.request.user

        
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(DiagnosticoCreateView, self).form_valid(form)



class DiagnosticoUpdateView(UpdateView):
    model = Diagnostico
    template_name = 'diagnostico/diagnostico_add.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('atencion:diagnostico_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(DiagnosticoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiagnosticoUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'diagnostico'
        context['title'] = _('Add %s') % _('Diagnostico')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(DiagnosticoUpdateView, self).form_valid(form)


class DiagnosticoDeleteView(DeleteView):
    model = Diagnostico
    success_url = reverse_lazy('atencion:pdiagnostico_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(DiagnosticoDeleteView, self).dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request,  ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)


            d.delete()
            msg = _(' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

# UnidadMedida==============================================================================

class UnidadMedidaListView(ListView):
    model = UnidadMedida
    template_name = 'unidad_medida/unidadmedida_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UnidadMedidaListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'codigo')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(UnidadMedidaListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'unidadmedida'
        context['title'] = _('Select %s to change') % capfirst(_('UnidadMedida'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class UnidadMedidaCreateView(CreateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'unidad_medida/unidadmedida_add.html'
    success_url = reverse_lazy('atencion:unidadmedida_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(UnidadMedidaCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UnidadMedidaCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'unidadmedida'
        context['title'] = ('Agregar %s') % ('UnidadMedida')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        self.object.usuario = self.request.user

        
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(UnidadMedidaCreateView, self).form_valid(form)



class UnidadMedidaUpdateView(UpdateView):
    model = UnidadMedida
    template_name = 'unidad_medida/unidadmedida_add.html'
    form_class = UnidadMedidaForm
    success_url = reverse_lazy('atencion:unidadmedida_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(UnidadMedidaUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UnidadMedidaUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'unidadmedida'
        context['title'] = _('Add %s') % _('UnidadMedida')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(UnidadMedidaUpdateView, self).form_valid(form)


class UnidadMedidaDeleteView(DeleteView):
    model = UnidadMedida
    success_url = reverse_lazy('atencion:periodo_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(UnidadMedidaDeleteView, self).dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request,  ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)


            d.delete()
            msg = _(' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

# class Consulta==============================================================================
"""
class ConsultaListView(ListView):
    model = Consulta
    template_name = 'consulta/consulta_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsultaListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'fecha')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(DiagnosticoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'diagnostio'
        context['title'] = _('Select %s to change') % capfirst(_('Diagnostico'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class DiagnosticoCreateView(CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'diagnostico/diagnostico_add.html'
    success_url = reverse_lazy('atencion:diagnostico_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(DiagnosticoCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiagnosticoCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'diagnostico'
        context['title'] = ('Agregar %s') % ('Diagnostico')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        self.object.usuario = self.request.user

        
        msg = _(' %(name)s "%(obj)s" fue creado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(DiagnosticoCreateView, self).form_valid(form)



class DiagnosticoUpdateView(UpdateView):
    model = Diagnostico
    template_name = 'diagnostico/diagnostico_add.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('atencion:diagnostico_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(DiagnosticoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiagnosticoUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'diagnostico'
        context['title'] = _('Add %s') % _('Diagnostico')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfactoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(DiagnosticoUpdateView, self).form_valid(form)


class DiagnosticoDeleteView(DeleteView):
    model = Diagnostico
    success_url = reverse_lazy('atencion:pdiagnostico_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(DiagnosticoDeleteView, self).dispatch(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            print(deps)
            if deps:
                messages.warning(self.request,  ('No se puede Eliminar %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)


            d.delete()
            msg = _(' %(name)s "%(obj)s" fue eliminado satisfactoriamente.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
"""
