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
from .forms.DistritoForm import (DistritoForm)
from .models import (
    Distrito)


# class Distrito

class DistritoListView(ListView):
    model = Distrito
    template_name = 'distrito/distrito_list.html'
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DistritoListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'nombre')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')

        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)


    def get_context_data(self, **kwargs):
        context = super(DistritoListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'distrito'
        context['title'] = _('Select %s to change') % capfirst(_('Distrito'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        return context


class DistritoCreateView(CreateView):
    model = Distrito
    form_class = DistritoForm
    template_name = 'distrito/distrito_add.html'
    success_url = reverse_lazy('atencion:distrito_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(DistritoCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DistritoCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'distrito'
        context['title'] = ('Agregar %s') % ('Distrito')
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
        return super(DistritoCreateView, self).form_valid(form)



class DistritoUpdateView(UpdateView):
    model = Distrito
    template_name = 'distrito/distrito_add.html'
    form_class = DistritoForm
    success_url = reverse_lazy('atencion:distrito_list')

    @method_decorator(permission_resource_required )
    def dispatch(self, request, *args, **kwargs):
        return super(DistritoUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DistritoUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'distrito'
        context['title'] = _('Add %s') % _('Distrito')
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.usuario = self.request.user


        msg = _('%(name)s "%(obj)s" fue cambiado satisfacoriamente.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(DistritoUpdateView, self).form_valid(form)


class DistritoDeleteView(DeleteView):
    model = Distrito
    success_url = reverse_lazy('atencion:distrito_list')


    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(DistritoDeleteView, self).dispatch(request, *args, **kwargs)


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
            msg = _(' %(name)s "%(obj)s" fuel eliminado satisfactorialmente.') % {
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