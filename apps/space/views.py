# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     space

Descripcion: Implementacion de los controladores de la app space
"""
import logging
log = logging.getLogger(__name__)
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.encoding import force_text
from django.utils.text import capfirst, get_text_list
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.db import transaction
from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponseRedirect
#from django.http import Http404
#from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from apps.utils.forms import empty
from apps.utils.security import SecurityKey, log_params, get_dep_objects, UserToken
from apps.utils.decorators import permission_resource_required

# models
from .models import Solution, Association, Enterprise, Headquar

# forms
from apps.space.forms import SolutionForm, AssociationForm, EnterpriseForm, \
    HeadquarForm, HeadquarAssociationForm

# others
import datetime
import json
#from unicodedata import normalize
#from django.utils import translation
#from django.utils import timezone
#from django.utils.timezone import get_current_timezone
#from django.conf import settings

# http://ccbv.co.uk/projects/Django/1.6/django.views.generic.edit
#context_object_name = 'pagex_obj'
# https://djangosnippets.org/snippets/73/ paginator

#from django.utils.html import escape, escapejs
#from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string


class HeadquarAssociationUpdateView(generic.edit.UpdateView):

    """ """
    model = Headquar
    form_class = HeadquarAssociationForm
    success_url = reverse_lazy('space:headquar-list')
    template_name = 'space/headquarassociation_form.html'

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'headquar_uas')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()

        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(HeadquarAssociationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            HeadquarAssociationUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'headquar'
        context['title'] = _('Change %s') % _('Association')
        try:
            association_name_list = json.dumps(
                list(col["name"] + "" for col in Association.objects.values("name").filter(is_active=True).order_by("name")))
        except Exception as e:
            messages.error(self.request, e)
        context['association_name_list'] = association_name_list
        return context

    def get_initial(self):
        initial = super(HeadquarAssociationUpdateView, self).get_initial()
        initial = initial.copy()
        initial['association_name'] = self.object.association.name
        return initial

    # TODO msg
    def form_valid(self, form):
        try:
            association_name = self.request.POST.get("association_name")
            try:
                form.instance.association = Association.objects.get(
                    name=association_name)
            except:
                raise Exception(
                    u"La asociación <b>%s</b> no existe, vuelva a intentar " %
                    (self.request.POST.get("association_name")))
            # salvar registro

            self.object = form.save(commit=True)
            msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.object)
            }
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
            return super(HeadquarAssociationUpdateView, self).form_valid(form)
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return super(HeadquarAssociationUpdateView, self).form_invalid(form)


class HeadquarUpdateActiveView(generic.View):

    """ """
    model = Headquar
    success_url = reverse_lazy('space:headquar-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        state = self.kwargs['state']
        pk = SecurityKey.is_valid_key(request, key, 'headquar_%s' % state)
        if not pk:
            return HttpResponseRedirect(self.success_url)
        try:
            self.object = self.model.objects.get(pk=pk)
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        msg = _('The %(name)s "%(obj)s" was %(action)s successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('reactivated') if state == 'rea' else _('inactivated'))
        }
        mse = _('The %(name)s "%(obj)s" is already %(action)s.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('active') if state == 'rea' else _('inactive'))
        }
        try:
            if state == 'ina' and not self.object.is_active:
                raise Exception(mse)
            else:
                if state == 'rea' and self.object.is_active:
                    raise Exception(mse)
                else:
                    self.object.is_active = (True if state == 'rea' else False)
                    self.object.save()
                    messages.success(self.request, msg)
                    log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)


class HeadquarCreateView(generic.edit.CreateView):

    """ """
    model = Headquar
    form_class = HeadquarForm
    success_url = reverse_lazy('space:headquar-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HeadquarCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HeadquarCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'headquar'
        context['title'] = _('Add %s') % _('Headquar')
        return context

    def form_valid(self, form):
        try:
            form.instance.association_id = UserToken.get_association_id(
                self.request.session)
            form.instance.enterprise_id = UserToken.get_enterprise_id(
                self.request.session)

            self.object = form.save(commit=True)
            msg = _('The %(name)s "%(obj)s" was added successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.object)
            }
            if self.object.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
            return super(HeadquarCreateView, self).form_valid(form)
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return super(HeadquarCreateView, self).form_invalid(form)


class HeadquarUpdateView(generic.edit.UpdateView):

    """ """
    model = Headquar
    form_class = HeadquarForm
    success_url = reverse_lazy('space:headquar-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'headquar_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()

        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(HeadquarUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HeadquarUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'headquar'
        context['title'] = _('Change %s') % _('Headquar')

        return context

    def form_valid(self, form):
        try:
            self.object = form.save(commit=True)
            msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.object)
            }
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
            return super(HeadquarUpdateView, self).form_valid(form)
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return super(HeadquarUpdateView, self).form_invalid(form)


class HeadquarListView(generic.ListView):

    """ """
    model = Headquar
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        enterprise_id = UserToken.get_enterprise_id(request.session)
        msg = _(u'%s is not selected or not found in the database.') % _(
            'Enterprise')
        try:
            Enterprise.objects.get(pk=enterprise_id)
        except Exception as e:
            messages.error(self.request, e)
            messages.warning(self.request, msg)
            return HttpResponseRedirect(reverse_lazy('accounts:index'))

        return super(HeadquarListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(
            enterprise_id=UserToken.get_enterprise_id(self.request.session)
        ).filter(**{column_contains: self.q}).order_by(self.o).distinct()

    def get_context_data(self, **kwargs):
        context = super(HeadquarListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'headquar'
        context['title'] = _('Select %s to change') % _('Headquar')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context

# region Enterprise OK


class EnterpriseUpdateActiveView(generic.View):

    """ """
    model = Enterprise
    success_url = reverse_lazy('space:enterprise-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        state = self.kwargs['state']
        pk = SecurityKey.is_valid_key(request, key, 'enterprise_%s' % state)
        if not pk:
            return HttpResponseRedirect(self.success_url)
        try:
            self.object = self.model.objects.get(pk=pk)
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        msg = _('The %(name)s "%(obj)s" was %(action)s successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('reactivated') if state == 'rea' else _('inactivated'))
        }
        mse = _('The %(name)s "%(obj)s" is already %(action)s.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('active') if state == 'rea' else _('inactive'))
        }
        try:
            if state == 'ina' and not self.object.is_active:
                raise Exception(mse)
            else:
                if state == 'rea' and self.object.is_active:
                    raise Exception(mse)
                else:
                    self.object.is_active = (True if state == 'rea' else False)
                    self.object.save()
                    messages.success(self.request, msg)
                    log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)


class EnterpriseDeleteView(generic.edit.BaseDeleteView):

    """ Elimina empresa con todas sus sedes """
    model = Enterprise
    success_url = reverse_lazy('space:enterprise-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'enterprise_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(EnterpriseDeleteView, self).dispatch(request, *args, **kwargs)

    # TODO msg
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            association = Association.objects.get(
                id=UserToken.get_association_id(request.session))
            if Enterprise.objects.filter(headquar__association_id=UserToken.get_association_id(request.session)).count() == 1:
                raise Exception(
                    (u"Asociación <b>%(name)s</b> no puede quedar sin ninguna sede asociada.") % {"name": association.name})

            d = self.get_object()
            # rastrear dependencias
            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request,  _('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)

            d.delete()
            msg = _('The %(name)s "%(obj)s" was deleted successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(d)
            }
            if not d.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class EnterpriseCreateView(generic.edit.CreateView):

    """ """
    model = Enterprise
    form_class = EnterpriseForm
    success_url = reverse_lazy('space:enterprise-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EnterpriseCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EnterpriseCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'enterprise'
        context['title'] = _('Add %s') % _('Enterprise')
        return context

    def get_form_kwargs(self):
        kwargs = super(EnterpriseCreateView, self).get_form_kwargs()
        kwargs['create'] = True
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            self.object = form.save(commit=True)
            headquar = Headquar()
            headquar.name = self.request.POST.get("sede")
            headquar.association_id = UserToken.get_association_id(
                self.request.session)
            headquar.enterprise = self.object
            headquar.save()

            msg = _('The %(name)s "%(obj)s" was added successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.object)
            }
            if self.object.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
            return super(EnterpriseCreateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return super(EnterpriseCreateView, self).form_invalid(form)


class EnterpriseListView(generic.ListView):

    """ """
    model = Enterprise
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        association_id = UserToken.get_association_id(request.session)
        msg = _(u'%s is not selected or not found in the database.') % _(
            'Association')
        try:
            Association.objects.get(pk=association_id)
        except Exception as e:
            messages.error(self.request, e)
            messages.warning(self.request, msg)
            return HttpResponseRedirect(reverse_lazy('accounts:index'))

        return super(EnterpriseListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(
            headquar__association_id=UserToken.get_association_id(
                self.request.session)
        ).annotate(num_sedes=Count("headquar")).filter(
            **{column_contains: self.q}).order_by(self.o).distinct()

    def get_context_data(self, **kwargs):
        context = super(EnterpriseListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'enterprise'
        context['title'] = _('Select %s to change') % _('Enterprise')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class EnterpriseUpdateView(generic.edit.UpdateView):

    """ """
    model = Enterprise
    form_class = EnterpriseForm
    success_url = reverse_lazy('space:enterprise-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get('pk', None)
        if key:
            pk = SecurityKey.is_valid_key(request, key, 'enterprise_upd')
            if not pk:
                return HttpResponseRedirect(self.success_url)
            self.kwargs['pk'] = pk
            try:
                self.get_object()
            except Exception as e:
                messages.error(self.request, e)
                return HttpResponseRedirect(self.success_url)
        else:
            self.kwargs['pk'] = UserToken.get_enterprise_id(request.session)
            self.success_url = reverse_lazy('space:enterprise-edit_current')
            msg = _(u'%s is not selected or not found in the database.') % _(
                'Enterprise')
            try:
                self.get_object()
            except Exception as e:
                messages.error(self.request, e)
                messages.warning(self.request, msg)
                return HttpResponseRedirect(reverse_lazy('accounts:index'))

        return super(EnterpriseUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EnterpriseUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'enterprise'
        context['title'] = _('Change %s') % (_('Enterprise') + ': ' +
                                             force_text(self.get_object()))

        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)
        log.warning(force_text(msg), extra=log_params(self.request))
        return super(EnterpriseUpdateView, self).form_valid(form)


class AssociationUpdateView(generic.edit.UpdateView):

    """ """
    model = Association
    form_class = AssociationForm
    success_url = reverse_lazy('space:association-edit_current')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        self.kwargs['pk'] = UserToken.get_association_id(request.session)
        msg = _(u'%s is not selected or not found in the database.') % _(
            'Association')
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            messages.warning(self.request, msg)
            return HttpResponseRedirect(reverse_lazy('accounts:index'))

        return super(AssociationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'association'
        context['title'] = _('Change %s') % (_('Association') + ': ' +
                                             force_text(self.get_object()))

        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)
        log.warning(force_text(msg), extra=log_params(self.request))
        return super(AssociationUpdateView, self).form_valid(form)


# region Solution OK

class SolutionUpdateActiveView(generic.View):

    """ """
    model = Solution
    success_url = reverse_lazy('space:solution-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        state = self.kwargs['state']
        pk = SecurityKey.is_valid_key(request, key, 'solution_%s' % state)
        if not pk:
            return HttpResponseRedirect(self.success_url)
        try:
            self.object = self.model.objects.get(pk=pk)
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        msg = _('The %(name)s "%(obj)s" was %(action)s successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('reactivated') if state == 'rea' else _('inactivated'))
        }
        mse = _('The %(name)s "%(obj)s" is already %(action)s.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object),
            'action': (_('active') if state == 'rea' else _('inactive'))
        }
        try:
            if state == 'ina' and not self.object.is_active:
                raise Exception(mse)
            else:
                if state == 'rea' and self.object.is_active:
                    raise Exception(mse)
                else:
                    self.object.is_active = (True if state == 'rea' else False)
                    self.object.save()
                    messages.success(self.request, msg)
                    log.warning(msg, extra=log_params(self.request))
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)


class SolutionDeleteView(generic.edit.BaseDeleteView):

    """ """
    model = Solution
    success_url = reverse_lazy('space:solution-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'solution_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(SolutionDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            # rastrear dependencias OK
            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request,  _('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)
            '''
            if d.module_set.count() > 0:
                raise Exception(
                    (u"Solucion <b>%(name)s</b> tiene modulos asignados.") % {"name": d.name})
            if d.association_set.count() > 0:
                raise Exception(
                    (u"Solucion <b>%(name)s</b> está asignado en asociaciones.") % {"name": d.name})
            if d.enterprise_set.count() > 0:
                raise Exception(
                    (u"Solucion <b>%(name)s</b> está asignado en empresas.") % {"name": d.name})
            '''
            d.delete()
            msg = _('The %(name)s "%(obj)s" was deleted successfully.') % {
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


class SolutionUpdateView(generic.edit.UpdateView):

    """ """
    model = Solution
    form_class = SolutionForm
    success_url = reverse_lazy('space:solution-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'solution_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
            '''
            ctx_dict = {'activation_key': 'eee',
                        'expiration_days': 2,
                        'site': 'localhost:8000'}
            subject = render_to_string(
                'registration/activation_email_subject.txt',
                ctx_dict)
            # Email subject *must not* contain newlines

            subject = ''.join(subject.splitlines())

            message = render_to_string(
                'registration/activation_email.txt', ctx_dict)
            send_mail(
                subject, message, settings.DEFAULT_FROM_EMAIL,
                ['asullom@gmail.com'], fail_silently=False)

            # send_mail(
            #    'Subject here', 'Here is the message.', 'asullom@gmail.com',
            #    ['asullom@gmail.com'], fail_silently=False)
            '''
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(SolutionUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SolutionUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'solution'
        context['title'] = _('Change %s') % _('Solution')

        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(SolutionUpdateView, self).form_valid(form)


class SolutionCreateView(generic.edit.CreateView):

    """ """
    model = Solution
    form_class = SolutionForm
    success_url = reverse_lazy('space:solution-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SolutionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SolutionCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'solution'

        context['now'] = datetime.datetime.now()
        context['title'] = _('Add %s') % _('Solution')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = _('The %(name)s "%(obj)s" was added successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        if self.object.id:
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))
        return super(SolutionCreateView, self).form_valid(form)


class SolutionListView(generic.ListView):

    """ """
    model = Solution
    paginate_by = settings.PER_PAGE

    #@method_decorator(login_required)
    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SolutionListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        #messages.success(self.request, _(u'saé'))
        context = super(SolutionListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'solution'
        context['title'] = _('Select %s to change') % _('Solution')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context
