# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad
https://docs.djangoproject.com/en/1.6/topics/forms/modelforms/
Descripcion: Implementacion de los controladores de la app sad
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
from django.db.models import Q
from django.http import HttpResponseRedirect
#from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from apps.utils.forms import empty
from apps.utils.security import SecurityKey, log_params, UserToken, get_dep_objects
from apps.utils.decorators import permission_resource_required

# models
from .models import Module, Menu, User, UserAssociation, UserEnterprise, \
    UserHeadquar, BACKEND, UserStatus, Ticket
# ModuleSolution, ModuleGroup

from apps.params.models import Person, NID, IDENTITY_TYPE_CHOICES
from apps.space.models import Solution, Headquar
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

# forms
from .forms import PermissionForm, GroupForm, ModuleForm, MenuForm, UserForm, \
    UserActiveUpdateForm, UserDetailForm

# TODO UserActiveUpdateView in progress

# region User


class PersonListView(generic.ListView):

    """ """
    model = Person
    paginate_by = settings.PER_PAGE
    template_name = 'sad/person_list.html'

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PersonListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'last_name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        user_list = User.objects.filter()

        return self.model.objects.exclude(user__in=user_list).filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = _('Select %s to change') % capfirst(_('Person'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


class UserDetailView(generic.DetailView):

    model = User

    success_url = reverse_lazy('sad:user-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'user_det')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        return super(UserDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = _('Detail %s') % capfirst(_('user'))

        #context['object'] = self.object

        if self.object.person:
            initial = {
                'username': self.object.username,
                'email': self.object.email,
                'is_superuser': self.object.is_superuser,
                'is_staff': self.object.is_staff,
                'is_active': self.object.is_active,
                'photo': self.object.person.photo,
                'first_name': self.object.person.first_name,
                'last_name': self.object.person.last_name,
                'identity_type': dict((x, y)
                                      for x, y in IDENTITY_TYPE_CHOICES)[
                                          self.object.person.identity_type],
                'identity_num': self.object.person.identity_num,
                'hgroups': UserHeadquar.objects.filter(user=self.object).order_by('headquar'),
                'egroups': UserEnterprise.objects.filter(user=self.object).order_by('enterprise'),
                'agroups': UserAssociation.objects.filter(user=self.object).order_by('association'),
                'status': UserStatus.objects.filter(user=self.object).order_by('-created_at'),
            }
        else:
            initial = {
                'username': self.object.username,
                'email': self.object.email,
                'is_superuser': self.object.is_superuser,
                'is_staff': self.object.is_staff,
                'is_active': self.object.is_active,
                'photo': '-',
                'first_name': '-',
                'last_name': '-',
                'identity_type': '-',
                'identity_num': '-',
                'hgroups': UserHeadquar.objects.filter(user=self.object).order_by('headquar'),
                'egroups': UserEnterprise.objects.filter(user=self.object).order_by('enterprise'),
                'agroups': UserAssociation.objects.filter(user=self.object).order_by('association'),
                'status': UserStatus.objects.filter(user=self.object).order_by('-created_at'),
            }
        context['form'] = UserDetailForm(initial=initial)
        return context


# TODO deshabilitar is_active
class UserActiveUpdateView(generic.edit.UpdateView):

    """ """
    model = User
    form_class = UserActiveUpdateForm
    template_name = 'sad/user_active_update_form.html'
    success_url = reverse_lazy('sad:user-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        #key = self.kwargs['pk']
        state = self.kwargs['state']
        #pk = SecurityKey.is_valid_key(request, key, 'user_upd')
        pk = SecurityKey.is_valid_key(request, key, 'user_%s' % state)
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            d = self.get_object()
            if d.username == 'admin':
                raise Exception(_('The %(name)s "%(obj)s" is protected') % {
                    'name': capfirst(force_text(self.model._meta.verbose_name)),
                    'obj': force_text(d)
                })

        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        return super(UserActiveUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserActiveUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = _('Change %s') % capfirst(_('user'))
        return context

    def get_form_kwargs(self):
        kwargs = super(UserActiveUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['object'] = self.object
        return kwargs

    def get_initial(self):
        initial = super(UserActiveUpdateView, self).get_initial()
        initial = initial.copy()
        d = self.object
        if d.is_active:
            initial['is_active'] = False
        else:
            initial['is_active'] = True
        return initial

    def form_valid(self, form):

        self.object = form.save(commit=False)

        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))

        return super(UserActiveUpdateView, self).form_valid(form)


class UserDeleteView(generic.edit.BaseDeleteView):

    """ Elimina module """
    model = User
    success_url = reverse_lazy('sad:user-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'user_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            if d.username == 'admin':
                raise Exception(_('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })

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
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class UserUpdateView(generic.edit.UpdateView):

    """ """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('sad:user-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'user_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        msg = _(u'%s is not selected or not found in the database.') % _(
            'Headquar')
        try:
            Headquar.objects.get(
                id=UserToken.get_headquar_id(self.request.session))
        except:
            messages.warning(self.request, msg)
            return HttpResponseRedirect(reverse_lazy('accounts:index'))

        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = _('Change %s') % capfirst(_('user'))
        return context

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['object'] = self.object
        return kwargs

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        initial = initial.copy()
        d = self.object
        if d.person:
            initial['photo'] = d.person.photo
            initial['first_name'] = d.person.first_name
            initial['last_name'] = d.person.last_name
            initial['identity_type'] = d.person.identity_type
            initial['identity_num'] = d.person.identity_num
            #initial['password1'] = ''
            #initial['password2'] = ''

        return initial

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            self.object = form.save(commit=False)
            try:
                person = Person.objects.get(pk=self.object.person.pk)
            except:
                person = Person()
                # person.save()
                pass

            person.first_name = form.cleaned_data['first_name']
            person.last_name = form.cleaned_data['last_name']
            person.identity_type = form.cleaned_data['identity_type']
            person.identity_num = form.cleaned_data['identity_num']
            person.photo = form.cleaned_data['photo']
            person.save()
            self.object.person = person

            self.object.save()
            d = self.object

            headquar = Headquar.objects.get(
                id=UserToken.get_headquar_id(self.request.session))

            # los permisos del usuario según su espacio
            group_id_list_by_user_and_headquar = list(col["id"] for col in Group.objects.values(
                "id").filter(userheadquar__headquar__id=headquar.id, userheadquar__user__id=d.id).distinct())
            group_id_list_by_user_and_enterprise = list(col["id"] for col in Group.objects.values("id").filter(
                userenterprise__enterprise__id=headquar.enterprise.id, userenterprise__user__id=d.id).distinct())
            group_id_list_by_user_and_association = list(col["id"] for col in Group.objects.values("id").filter(
                userassociation__association__id=headquar.association.id, userassociation__user__id=d.id).distinct())

            # Elimino los antiguos privilegios
            group_id_list_by_user_and_hea = list(
                set(group_id_list_by_user_and_headquar + group_id_list_by_user_and_enterprise +
                    group_id_list_by_user_and_association))

            for group_id in group_id_list_by_user_and_headquar:
                group = Group.objects.get(id=group_id)
                user_profile_headquar = UserHeadquar.objects.get(
                    user_id=d.id, group_id=group_id, headquar_id=headquar.id)
                user_profile_headquar.delete()

            for group_id in group_id_list_by_user_and_enterprise:
                group = Group.objects.get(id=group_id)
                user_profile_enterprise = UserEnterprise.objects.get(
                    user_id=d.id, group_id=group_id, enterprise_id=headquar.enterprise.id)
                user_profile_enterprise.delete()

            for group_id in group_id_list_by_user_and_association:
                group = Group.objects.get(id=group_id)
                user_profile_association = UserAssociation.objects.get(
                    user_id=d.id, group_id=group_id, association_id=headquar.association.id)
                user_profile_association.delete()

            for group_id in group_id_list_by_user_and_hea:
                group = Group.objects.get(id=group_id)
                d.groups.remove(group)

            # agregando en UserHeadquar
            groups_sede = self.request.POST.getlist("hgroups")
            groups_sede = list(set(groups_sede))
            for value in groups_sede:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_headquar = UserHeadquar()
                user_profile_headquar.user = d
                user_profile_headquar.headquar = headquar
                user_profile_headquar.group = group
                user_profile_headquar.save()

            # agregando en UserEnterprise
            groups_enterprise = self.request.POST.getlist("egroups")
            groups_enterprise = list(set(groups_enterprise))
            for value in groups_enterprise:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_enterprise = UserEnterprise()
                user_profile_enterprise.user = d
                user_profile_enterprise.enterprise = headquar.enterprise
                user_profile_enterprise.group = group
                user_profile_enterprise.save()

            # agregando en UserAssociation
            groups_association = self.request.POST.getlist("agroups")
            groups_association = list(set(groups_association))
            for value in groups_association:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_association = UserAssociation()
                user_profile_association.user = d
                user_profile_association.association = headquar.association
                user_profile_association.group = group
                user_profile_association.save()

            # agregando en user_groups
            group_dist_list = list(
                set(groups_sede + groups_enterprise + groups_association))
            for value in group_dist_list:
                group = Group.objects.get(id=value)
                d.groups.add(group)

            msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.object)
            }
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))

            return super(UserUpdateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return super(UserUpdateView, self).form_invalid(form)


class UserCreateView(generic.edit.CreateView):

    """  """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('sad:user-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        msg = _(u'%s is not selected or not found in the database.') % _(
            'Headquar')
        try:
            Headquar.objects.get(
                id=UserToken.get_headquar_id(self.request.session))
        except:
            messages.warning(self.request, msg)
            return HttpResponseRedirect(reverse_lazy('accounts:index'))

        key = self.kwargs.get('pk', None)
        self.person_pk = None
        if key:
            self.person_pk = SecurityKey.is_valid_key(
                self.request, key, 'user_cre')
            if not self.person_pk:
                return HttpResponseRedirect(reverse_lazy('sad:user-person_search'))

        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = _('Add %s') % capfirst(_('user'))
        return context

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = super(UserCreateView, self).get_initial()
        initial = initial.copy()

        if self.person_pk:
            d = Person.objects.get(pk=self.person_pk)
            if d:
                initial['photo'] = d.photo
                initial['first_name'] = d.first_name
                initial['last_name'] = d.last_name
                initial['identity_type'] = d.identity_type
                initial['identity_num'] = d.identity_num
                initial['person_id'] = d.pk
                #initial['password2'] = ''

        return initial

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:

            t = Ticket(
                text='san',
                row=1,
                user=self.request.user
            )
            t.save()
            #raise Exception('eeee')
            try:
                person = Person.objects.get(
                    pk=self.request.POST.get("person_id"))
            except Exception as e:
                person = Person()
                person.save()
                pass
            person.first_name = form.cleaned_data['first_name']
            person.last_name = form.cleaned_data['last_name']
            person.identity_type = form.cleaned_data['identity_type']
            person.identity_num = form.cleaned_data['identity_num']
            person.photo = form.cleaned_data['photo']

            # Personalizando los mensajes de error para los Field form
            '''
            if Person.objects.exclude(id=person.id).filter(identity_type=person.identity_type, identity_num=person.identity_num).count() > 0:
                form._errors['identity_type'] = form.error_class([
                    _(u'%(model_name)s with this %(field_label)s already exists.') % {
                        'model_name': _('Person'),
                        'field_label': get_text_list((capfirst(_('Type')), capfirst(_('number'))), _('and')),
                    }
                ])
                form._errors['identity_num'] = form.error_class([
                    _(u'%(model_name)s with this %(field_label)s already exists.') % {
                        'model_name': _('Person'),
                        'field_label': get_text_list((capfirst(_('number')), capfirst(_('Type'))), _('and')),
                    }
                ])
                transaction.savepoint_rollback(sid)
                return super(UserCreateView, self).form_invalid(form)
            '''
            person.save()
            self.object = form.save(commit=False)
            self.object.person = person

            self.object.save()
            d = self.object

            headquar = Headquar.objects.get(
                id=UserToken.get_headquar_id(self.request.session))

            # agregando en UserHeadquar
            groups_sede = self.request.POST.getlist("hgroups")
            groups_sede = list(set(groups_sede))
            for value in groups_sede:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_headquar = UserHeadquar()
                user_profile_headquar.user = d
                user_profile_headquar.headquar = headquar
                user_profile_headquar.group = group
                user_profile_headquar.save()

            # agregando en UserEnterprise
            groups_enterprise = self.request.POST.getlist("egroups")
            groups_enterprise = list(set(groups_enterprise))
            for value in groups_enterprise:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_enterprise = UserEnterprise()
                user_profile_enterprise.user = d
                user_profile_enterprise.enterprise = headquar.enterprise
                user_profile_enterprise.group = group
                user_profile_enterprise.save()

            # agregando en UserAssociation
            groups_association = self.request.POST.getlist("agroups")
            groups_association = list(set(groups_association))
            for value in groups_association:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_association = UserAssociation()
                user_profile_association.user = d
                user_profile_association.association = headquar.association
                user_profile_association.group = group
                user_profile_association.save()

            # agregando en user_groups
            group_dist_list = list(
                set(groups_sede + groups_enterprise + groups_association))
            for value in group_dist_list:
                group = Group.objects.get(id=value)
                d.groups.add(group)

            msg = _('The %(name)s "%(obj)s" was added successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.object)
            }
            if self.object.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
            return super(UserCreateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return super(UserCreateView, self).form_invalid(form)


class UserListView(generic.ListView):

    """ """
    model = User
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'username')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o).with_status()

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'user'
        context['title'] = _('Select %s to change') % capfirst(_('user'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


# region Menu OK
class MenuUpdateActiveView(generic.View):

    """ """
    model = Menu
    success_url = reverse_lazy('sad:menu-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        state = self.kwargs['state']
        pk = SecurityKey.is_valid_key(request, key, 'menu_%s' % state)
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


class MenuDeleteView(generic.edit.BaseDeleteView):

    """ Elimina module """
    model = Menu
    success_url = reverse_lazy('sad:menu-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'menu_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(MenuDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request,  _('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })
                raise Exception(msg)

            if d.id <= 100:
                raise Exception(_('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(d) + '"'
                })

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


class MenuUpdateView(generic.edit.UpdateView):

    """ """
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy('sad:menu-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'menu_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        return super(MenuUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MenuUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'menu'
        context['title'] = _('Change %s') % _('Menu')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))

        return super(MenuUpdateView, self).form_valid(form)


class MenuCreateView(generic.edit.CreateView):

    """  """
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy('sad:menu-list')

    #@method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MenuCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'menu'
        context['title'] = _('Add %s') % _('Menu')
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
        return super(MenuCreateView, self).form_valid(form)


class MenuListView(generic.ListView):

    """ """
    model = Menu
    paginate_by = settings.PER_PAGE

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', 'pos')
        self.f = empty(self.request, 'f', 'title')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)

    def get_context_data(self, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'menu'
        context['title'] = _('Select %s to change') % _('menu')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


# region Module OK
class ModuleSolutionsUpdateView(generic.ListView):

    """ """
    model = Module  # rows
    # modulesolutions es el controller
    template_name = 'sad/modulesolutions_form.html'
    success_url = reverse_lazy('sad:modulesolutions-update')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ModuleSolutionsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(is_active=True).filter(**{column_contains: self.q}).order_by(self.o)
        # return self.model.objects.filter(is_active=True).order_by('-id')

    def get_context_data(self, **kwargs):
        try:
            # Module.objects.filter(is_active=True).order_by("module")
            module_list = self.get_queryset()
            solution_list = Solution.objects.filter(
                is_active=True).order_by('-id')
            # obtener los permissions del group para mostrarlos
            privilegios = []
            for m in module_list:
                for s in m.solutions.all():
                    privilegios.append('%s-%s' % (s.id, m.id))
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        context = super(
            ModuleSolutionsUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'modulesolutions'
        context['title'] = _('Select %s to change') % _('Module')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        context['solution_list'] = solution_list
        context['privilegios'] = privilegios
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            sid = transaction.savepoint()
            '''
            group_list = Group.objects.all().order_by('-id')
            old_privilegios_r = []
            for g in group_list:
                for p in g.permissions.all():
                    old_privilegios_r.append('%s-%s' % (p.id, g.id))
            '''
            old_privilegios_r = request.POST.get('old_privilegios')
            if old_privilegios_r:
                old_privilegios_r = old_privilegios_r.split(',')

            # Elimino los antiguos privilegios
            for value in old_privilegios_r:
                # el formato es 1-4 = solution_id-module_id
                data = value.split("-")
                module = Module.objects.get(id=data[1])
                solution = Solution.objects.get(id=data[0])
                # ModuleSolution.objects.get(
                #    module=module, solution=solution).delete()
                module.solutions.remove(solution)

            privilegios_r = request.POST.getlist('privilegios')
            for value in privilegios_r:
                # el formato es 1-4 = solution_id-module_id
                data = value.split("-")
                module = Module.objects.get(id=data[1])
                solution = Solution.objects.get(id=data[0])
                #ModuleSolution.objects.create(module=module, solution=solution)
                module.solutions.add(solution)

            msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
                'name': '',
                'obj': capfirst(_('permissions'))
            }
            messages.success(self.request, msg)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))

        return HttpResponseRedirect(self.success_url)


class ModuleUpdateActiveView(generic.View):

    """ """
    model = Module
    success_url = reverse_lazy('sad:module-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        state = self.kwargs['state']
        pk = SecurityKey.is_valid_key(request, key, 'module_%s' % state)
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


class ModuleDeleteView(generic.edit.BaseDeleteView):

    """ Elimina module """
    model = Module
    success_url = reverse_lazy('sad:module-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'module_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(ModuleDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
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
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ModuleUpdateView(generic.edit.UpdateView):

    """ """
    model = Module
    form_class = ModuleForm
    success_url = reverse_lazy('sad:module-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'module_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)

        return super(ModuleUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModuleUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'module'
        context['title'] = _('Change %s') % _('Module')

        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        '''
        ModuleGroup.objects.filter(module=self.object).delete()
        for other_side_model_object in form.cleaned_data['groups']:
            intermediate_model = ModuleGroup()
            intermediate_model.module = self.object
            intermediate_model.group = other_side_model_object
            intermediate_model.save()
        '''
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))

        return super(ModuleUpdateView, self).form_valid(form)


class ModuleCreateView(generic.edit.CreateView):

    """  """
    model = Module
    form_class = ModuleForm
    success_url = reverse_lazy('sad:module-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ModuleCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModuleCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'module'
        context['title'] = _('Add %s') % _('Module')
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
        return super(ModuleCreateView, self).form_valid(form)


class ModuleListView(generic.ListView):

    """ """
    model = Module

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ModuleListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModuleListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'module'
        context['title'] = _('Select %s to change') % _('Module')
        return context


# region Group OK
class GroupPermissionsUpdateView(generic.ListView):

    """ """
    model = Permission
    # grouppermissions es el controller
    template_name = 'sad/grouppermissions_form.html'
    success_url = reverse_lazy('sad:grouppermissions-update')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupPermissionsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'name')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}).order_by(self.o)
        # return self.model.objects.all().order_by("content_type__app_label",
        # "content_type__model")

    def get_context_data(self, **kwargs):
        try:
            group_list = Group.objects.all().order_by('-id')
            # obtener los permissions del group para mostrarlos
            privilegios = []
            for g in group_list:
                for p in g.permissions.all():
                    privilegios.append('%s-%s' % (p.id, g.id))
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        context = super(
            GroupPermissionsUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'grouppermissions'
        context['title'] = _('Select %s to change') % _('permissions')

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')

        context['group_list'] = group_list
        context['privilegios'] = privilegios
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            sid = transaction.savepoint()
            '''
            group_list = Group.objects.all().order_by('-id')
            old_privilegios_r = []
            for g in group_list:
                for p in g.permissions.all():
                    old_privilegios_r.append('%s-%s' % (p.id, g.id))
            '''
            old_privilegios_r = request.POST.get('old_privilegios')
            if old_privilegios_r:
                old_privilegios_r = old_privilegios_r.split(',')

            # Elimino los antiguos privilegios
            for value in old_privilegios_r:
                # el formato es 1-4 = recurso_id-perfil_id
                data = value.split('-')
                group = Group.objects.get(id=data[1])
                recur = Permission.objects.get(id=data[0])
                group.permissions.remove(recur)

            privilegios_r = request.POST.getlist('privilegios')
            for value in privilegios_r:
                # el formato es 1-4 = recurso_id-perfil_id
                data = value.split('-')
                group = Group.objects.get(id=data[1])
                recur = Permission.objects.get(id=data[0])
                group.permissions.add(recur)
            msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
                'name': '',
                'obj': capfirst(_('permissions'))
            }
            messages.success(self.request, msg)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))

        return HttpResponseRedirect(self.success_url)


class GroupDeleteView(generic.edit.BaseDeleteView):

    """ Elimina group """
    model = Group
    success_url = reverse_lazy('sad:group-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'group_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(GroupDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
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
            messages.error(request, e)
            log.warning(force_text(e), extra=log_params(self.request))
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class GroupUpdateView(generic.edit.UpdateView):

    """ """
    model = Group
    form_class = GroupForm
    template_name = 'sad/group_form.html'
    success_url = reverse_lazy('sad:group-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'group_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(GroupUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'group'
        context['title'] = _('Change %s') % capfirst(_('group'))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=True)
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
            'name': capfirst(force_text(self.model._meta.verbose_name)),
            'obj': force_text(self.object)
        }
        messages.success(self.request, msg)
        log.warning(msg, extra=log_params(self.request))
        return super(GroupUpdateView, self).form_valid(form)


class GroupCreateView(generic.edit.CreateView):

    """  """
    model = Group
    form_class = GroupForm
    template_name = 'sad/group_form.html'
    success_url = reverse_lazy('sad:group-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'group'
        context['title'] = _('Add %s') % capfirst(_('group'))
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
        return super(GroupCreateView, self).form_valid(form)


class GroupListView(generic.ListView):

    """ """
    model = Group
    paginate_by = settings.PER_PAGE
    template_name = 'sad/group_list.html'

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupListView, self).dispatch(request, *args, **kwargs)

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
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'group'
        context['title'] = _('Select %s to change') % capfirst(_('group'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context


# region Permission OK
class PermissionDeleteView(generic.edit.BaseDeleteView):

    """ Elimina permission """
    model = Permission
    success_url = reverse_lazy('sad:permission-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs['pk']
        pk = SecurityKey.is_valid_key(request, key, 'permission_del')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            d = self.get_object()
            self.recurso = '/%s/' % d.content_type.app_label
            if d.codename:
                self.recurso = '/%s/%s/' % (
                    d.content_type.app_label, d.content_type.name)
                codename_list = d.codename.split('_', 1)
                if len(codename_list) > 1:
                    self.recurso = '/%s/%s/%s/' % (
                        d.content_type.app_label, d.content_type.name,
                        codename_list[1]
                    )
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(PermissionDeleteView, self).dispatch(request, *args,
                                                          **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            d = self.get_object()
            # rastreando dependencias
            deps, msg = get_dep_objects(d)
            if deps:
                messages.warning(self.request,  _('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(self.recurso) + '"'
                })
                raise Exception(msg)
            if d.id <= 100:
                raise Exception(_('Cannot delete %(name)s') % {
                    "name": capfirst(force_text(self.model._meta.verbose_name))
                    + ' "' + force_text(self.recurso) + '"'
                })

            d.delete()
            msg = _('The %(name)s "%(obj)s" was deleted successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(self.recurso)
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


class PermissionUpdateView(generic.edit.UpdateView):

    """ """
    model = Permission
    form_class = PermissionForm
    template_name = 'sad/permission_form.html'
    success_url = reverse_lazy('sad:permission-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        pk = SecurityKey.is_valid_key(request, key, 'permission_upd')
        if not pk:
            return HttpResponseRedirect(self.success_url)
        self.kwargs['pk'] = pk
        try:
            self.get_object()
        except Exception as e:
            messages.error(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return HttpResponseRedirect(self.success_url)
        return super(PermissionUpdateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(PermissionUpdateView, self).get_initial()
        initial = initial.copy()
        d = self.object
        initial['app_label'] = d.content_type.app_label
        initial['controller_view'] = d.content_type.name
        codename_list = d.codename.split('_', 1)
        if len(codename_list) > 1:
            initial['action_view'] = codename_list[1]
        return initial

    def get_context_data(self, **kwargs):
        context = super(PermissionUpdateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'permission'
        context['title'] = _('Change %s') % capfirst(_('permission'))
        return context

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:

            form.instance.codename = form.cleaned_data['codename']
            content_type, is_c_t_created = ContentType.objects.get_or_create(
                # name=form.cleaned_data['controller_view'].lower(),
                model=form.cleaned_data['controller_view'].lower(),
                app_label=form.cleaned_data['app_label'].lower(),
            )
            form.instance.content_type = content_type
            if Permission.objects.exclude(id=self.object.id).filter(
                codename=form.cleaned_data[
                    'codename'], content_type=content_type
            ).count() > 0:
                form._errors['controller_view'] = form.error_class([
                    _(u'%(model_name)s with this %(field_label)s already exists.') % {
                        'model_name': capfirst(_('permission')),
                        'field_label': form.cleaned_data['recurso'],
                    }
                ])

                transaction.savepoint_rollback(sid)
                return super(PermissionUpdateView, self).form_invalid(form)

            self.object = form.save(commit=True)
            msg = _('The %(name)s "%(obj)s" was changed successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(form.cleaned_data['recurso'])
            }
            messages.success(self.request, msg)
            log.warning(msg, extra=log_params(self.request))

            return super(PermissionUpdateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return super(PermissionUpdateView, self).form_invalid(form)


class PermissionCreateView(generic.edit.CreateView):

    """  """
    model = Permission
    form_class = PermissionForm
    template_name = 'sad/permission_form.html'
    success_url = reverse_lazy('sad:permission-list')

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PermissionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PermissionCreateView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'permission'
        context['title'] = _('Add %s') % capfirst(_('permission'))
        return context

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:

            form.instance.codename = form.cleaned_data['codename']
            content_type, is_c_t_created = ContentType.objects.get_or_create(
                # name=form.cleaned_data['controller_view'].lower(),
                model=form.cleaned_data['controller_view'].lower(),
                app_label=form.cleaned_data['app_label'].lower(),
            )
            form.instance.content_type = content_type

            if Permission.objects.filter(
                codename=form.cleaned_data['codename'].lower(),
                content_type=content_type).count() > 0:
                form._errors['controller_view'] = form.error_class([
                    _(u'%(model_name)s with this %(field_label)s already exists.') % {
                        'model_name': capfirst(_('permission')),
                        'field_label': form.cleaned_data['recurso'],
                    }
                ])
                transaction.savepoint_rollback(sid)
                return super(PermissionCreateView, self).form_invalid(form)

            self.object = form.save(commit=True)
            msg = _('The %(name)s "%(obj)s" was added successfully.') % {
                'name': capfirst(force_text(self.model._meta.verbose_name)),
                'obj': force_text(form.cleaned_data['recurso'])
            }
            if self.object.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
            return super(PermissionCreateView, self).form_valid(form)
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            log.warning(force_text(e), extra=log_params(self.request))
            return super(PermissionCreateView, self).form_invalid(form)


class PermissionListView(generic.ListView):

    """ """
    model = Permission
    paginate_by = settings.PER_PAGE
    template_name = 'sad/permission_list.html'

    @method_decorator(permission_resource_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PermissionListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        if 'all' in self.request.GET:
            return None
        return generic.ListView.get_paginate_by(self, queryset)

    def get_queryset(self):
        self.o = empty(self.request, 'o', '-id')
        self.f = empty(self.request, 'f', 'content_type__app_label')
        self.q = empty(self.request, 'q', '')
        column_contains = u'%s__%s' % (self.f, 'contains')
        return self.model.objects.filter(**{column_contains: self.q}
                                         ).order_by(self.o, 'content_type__model')

    def get_context_data(self, **kwargs):
        context = super(PermissionListView, self).get_context_data(**kwargs)
        context['opts'] = self.model._meta
        context['cmi'] = 'permission'
        context['title'] = _('Select %s to change') % capfirst(_('permission'))

        context['o'] = self.o
        context['f'] = self.f
        context['q'] = self.q.replace('/', '-')
        return context
