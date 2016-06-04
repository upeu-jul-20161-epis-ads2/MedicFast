# _*_ coding: utf-8 _*_
import logging

from django.http.response import HttpResponse

log = logging.getLogger(__name__)
from django.utils.translation import ugettext as _  # , ungettext
from django.utils.encoding import force_text
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from apps.utils.forms import empty
from apps.utils.security import SecurityKey, log_params, UserToken
from apps.utils.decorators import permission_resource_required

# models
from apps.sad.models import User, Module, UserAssociation, UserEnterprise, \
    UserHeadquar, BACKEND, HOTEL
from apps.params.models import Person, NID, IDENTITY_TYPE_CHOICES
from apps.space.models import Association, Enterprise, Headquar, Solution
from django.contrib.auth.models import Group
# forms
from .forms import LoginForm, RegistrationForm, \
    RegistrationEnterpriseAssociationForm

# otros
from django.contrib.auth import authenticate, login, logout
from unicodedata import normalize
from django.db.models import Q
from django.views.decorators.cache import never_cache


class EnterpriseAssociationCreateView(generic.CreateView):

    """ """
    form_class = RegistrationEnterpriseAssociationForm
    success_url = reverse_lazy('accounts:index')
    model = Enterprise
    template_name = 'accounts/enterpriseassociation_form.html'

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:
            association = Association(
                name=form.cleaned_data['association_name'],
                type_a=form.cleaned_data['type_e'],
                solution=form.cleaned_data['solution'])
            association.save()

            self.object = form.save(commit=False)
            self.object.save()
            headquar = Headquar(
                name="Principal",
                association=association,
                enterprise=self.object)
            headquar.save()

            solution_id = self.request.POST.get("solution")
            solution = Solution.objects.get(pk=solution_id)

            # asigna permisos al usuario para manipular datos de cierta sede,
            # empresa o asociación
            user = self.request.user
            enterprise = self.object
            group_dist_list = []
            for module in solution.module_set.all():  # .distinct()
                for group in module.initial_groups.all():
                    if len(group_dist_list) == 0:
                        group_dist_list.append(group.id)
                        user.groups.add(group)

                        user_association = UserAssociation()
                        user_association.user = user
                        user_association.association = association
                        user_association.group = group
                        user_association.save()

                        user_enterprise = UserEnterprise()
                        user_enterprise.user = user
                        user_enterprise.enterprise = enterprise
                        user_enterprise.group = group
                        user_enterprise.save()

                        user_headquar = UserHeadquar()
                        user_headquar.user = user
                        user_headquar.headquar = headquar
                        user_headquar.group = group
                        user_headquar.save()
                    else:
                        if group.id not in group_dist_list:
                            group_dist_list.append(group.id)
                            user.groups.add(group)

                            user_association = UserAssociation()
                            user_association.user = user
                            user_association.association = association
                            user_association.group = group
                            user_association.save()

                            user_enterprise = UserEnterprise()
                            user_enterprise.user = user
                            user_enterprise.enterprise = enterprise
                            user_enterprise.group = group
                            user_enterprise.save()

                            user_headquar = UserHeadquar()
                            user_headquar.user = user
                            user_headquar.headquar = headquar
                            user_headquar.group = group
                            user_headquar.save()

            msg = _('The %(name)s "%(obj)s" was added successfully.') % {
                'name': force_text(self.model._meta.verbose_name),
                'obj': force_text(self.object)
            }

            if self.object.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
            return super(EnterpriseAssociationCreateView, self).form_valid(form)

        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            log.warning(e, extra=log_params(self.request))
            return super(EnterpriseAssociationCreateView, self).form_invalid(form)


@login_required(login_url="/accounts/login/")
def load_access(request, headquar_id, module_id):
    if request.is_ajax():
        return HttpResponse("ESTA OPERACION NO DEBE SER CARGADO CON AJAX, Presione F5")
    else:
        try:
            try:
                headquar = Headquar.objects.get(id=headquar_id)
            except:
                messages.error(
                    request, _(u'%s is not selected or not found in the database.') %
                    _('Headquar'))
                return HttpResponseRedirect("/accounts/")
            try:
                module = Module.objects.get(id=module_id)
            except:
                messages.error(
                    request, _(u'%s is not selected or not found in the database.') %
                    _('Module'))
                return HttpResponseRedirect("/accounts/")

            # vovler a verificar si tiene permisos
            if not request.user.is_superuser:
                # obteniendo las sedes a la cual tiene acceso
                headquar_list = Headquar.objects.filter(
                    userheadquar__user__id=request.user.id).distinct()
                if headquar not in headquar_list:
                    raise Exception(
                        _(u'Permission denied. You don\'t have permission to %s.' % (headquar.enterprise.name + ' ' + headquar.name)))
                # obteniendo los módulos a la cual tiene acceso
                group_list = Group.objects.filter(
                    userheadquar__headquar__id=headquar.id, userheadquar__user__id=request.user.id).distinct()
                module_list = Module.objects.filter(
                    groups__in=group_list).distinct()

                if module not in module_list:
                    raise Exception(
                        _(u'Permission denied. You don\'t have permission to %s.' %
                                   (module.name + ' ' + headquar.enterprise.name + _(' in ')+ headquar.name)))

            # cargando permisos de datos para el usuario
            UserToken.set_association_id(request, headquar.association.id)
            UserToken.set_enterprise_id(request, headquar.enterprise.id)
            UserToken.set_headquar_id(request, headquar.id)

            try:
                user = User.objects.get(pk=request.user.id)
                if user.id:
                    user.last_headquar_id = headquar_id
                    user.last_module_id = module_id
                    user.save()
            except:
                '''
                person = Person(first_name=request.user.first_name, last_name=request.user.last_name)
                person.save()

                profile = Profile(user=request.user, last_headquar_id=headquar_id, last_module_id=module_id)
                profile.person = person
                profile.save()
                '''
                pass

            # messages.info(request, ("La sede %(name)s ha sido cargado correctamente.") % {"name":headquar_id} )
            if BACKEND == module.module:
                return HttpResponseRedirect("/mod_backend/dashboard/")
            
            if HOTEL == module.module:
                return HttpResponseRedirect( "/mod_hotel/dashboard")

            # if VENTAS == module.module:
            #    return HttpResponseRedirect( "/mod_ventas/dashboard/")
            # if PRO == module.module:
            #    return HttpResponseRedirect( "/mod_pro/dashboard/")
            # TODO agregue aqui su nuevo modulo
            else:
                messages.error(request, 'Not implemented %s') %_('Module')
                #raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_full_name() module')
                return HttpResponseRedirect("/accounts/")
        except Exception as e:
            messages.error(request, e)
        return HttpResponseRedirect("/accounts/")


@login_required
def index(request):
    """
    """
    o = empty(request, 'o', 'enterprise__name')
    f = empty(request, 'f', 'enterprise__name')
    q = empty(request, 'q', '')
    column_contains = u'%s__%s' % (f, 'contains')

    headquar_list_by_user = []
    headquar_list = []
    if request.user.is_superuser:
        headquar_list = Headquar.objects.filter(**{column_contains: q}).order_by(
            "-association__name", "-enterprise__name", "-id").distinct()  # Trae todo
    else:
        if request.user.id:
            # print "--%s" % request.user.id
            headquar_list = Headquar.objects.filter(**{column_contains: q}).filter(userheadquar__user__id=request.user.id).order_by(
                "-association__name", "-enterprise__name", "-id").distinct()  # request.user.id
    for headquar in headquar_list:
        group_list = Group.objects.filter(
            userheadquar__headquar__id=headquar.id, userheadquar__user__id=request.user.id).distinct()
        module_list = Module.objects.filter(groups__in=group_list).distinct()
        if request.user.is_superuser:
            """
            permitir ingresar al módulo:Django Backend 
            """
            if len(module_list) == 0:
                module_list = Module.objects.filter(
                    module=BACKEND).distinct()
            else:
                if Module.objects.get(module=BACKEND) not in module_list:
                    module_list = Module.objects.filter(
                        Q(groups__in=group_list) | Q(module=BACKEND)).distinct()

        headquar_list_by_user.append({
            "association": headquar.association,
            "enterprise": headquar.enterprise,
            "headquar": headquar,
            "modules": module_list,
            "groups": group_list,
        })
    c = {
        'opts': _('Home'),
        'cmi': 'accounts:index',
        'title': _('Select %s to change') % _('Module'),

        "object_list": headquar_list_by_user,

        'o': o,
        'f': f,
        'q': q.replace('/', '-'),

    }
    return render(request, 'accounts/index.html', c)


class LoginView(generic.FormView):

    """ """
    form_class = LoginForm
    success_url = reverse_lazy('accounts:index')
    template_name = 'registration/login.html'

    @never_cache
    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated() and self.request.user.is_active:
            if self.request.GET.get('next'):
                self.success_url = self.request.GET.get('next')
            else:
                self.success_url = '/accounts/'
                try:  # intentar cargar la última session
                    user = User.objects.get(pk=self.request.user.id)
                    if user.last_headquar_id and user.last_module_id:
                        self.success_url = "/accounts/load_access/%s/%s/" % (
                            user.last_headquar_id, user.last_module_id)
                except:
                    pass
            return HttpResponseRedirect(self.success_url)

        self.request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:

            if not form.cleaned_data.get('remember_me'):
                self.request.session.set_expiry(0)

            login(self.request, user)
            messages.success(self.request, _('Welcome,') + ' ' + username)

            if self.request.GET.get('next'):
                self.success_url = self.request.GET.get('next')
            else:
                self.success_url = '/accounts/'
                try:  # intentar cargar la última session
                    user = User.objects.get(pk=self.request.user.id)
                    if user.last_headquar_id and user.last_module_id:
                        # self.success_url = reverse_lazy('hotel:list')
                        self.success_url = "/accounts/load_access/%s/%s/" % (
                            user.last_headquar_id, user.last_module_id)
                except:
                    pass
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(generic.RedirectView):

    """ """
    url = reverse_lazy('home:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


class SignUpView(generic.CreateView):

    """ """
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    model = User
    template_name = 'registration/registration_form.html'

    @transaction.atomic
    def form_valid(self, form):
        sid = transaction.savepoint()
        try:

            person = Person(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                identity_type=NID,
                identity_num=form.cleaned_data['identity_num'],
                photo=form.cleaned_data['photo'])
            person.save()

            self.object = form.save(commit=False)
            self.object.person = person

            association = Association(
                name=form.cleaned_data['association_name'],
                type_a=form.cleaned_data['enterprise_type_e'],
                solution=form.cleaned_data['solution'])
            association.save()

            enterprise = Enterprise(
                name=form.cleaned_data['enterprise_name'],
                tax_id=form.cleaned_data['enterprise_tax_id'],
                type_e=form.cleaned_data['enterprise_type_e'],
                solution=form.cleaned_data['solution'])
            enterprise.save()

            headquar = Headquar(
                name="Principal",
                association=association,
                enterprise=enterprise)
            headquar.save()

            solution_id = self.request.POST.get("solution")
            solution = Solution.objects.get(pk=solution_id)

            # asigna permisos al usuario para manipular datos de cierta sede,
            # empresa o asociación
            self.object.save()
            user = self.object
            group_dist_list = []
            for module in solution.module_set.all():  # .distinct()
                for group in module.initial_groups.all():
                    if len(group_dist_list) == 0:
                        group_dist_list.append(group.id)
                        user.groups.add(group)

                        user_association = UserAssociation()
                        user_association.user = user
                        user_association.association = association
                        user_association.group = group
                        user_association.save()

                        user_enterprise = UserEnterprise()
                        user_enterprise.user = user
                        user_enterprise.enterprise = enterprise
                        user_enterprise.group = group
                        user_enterprise.save()

                        user_headquar = UserHeadquar()
                        user_headquar.user = user
                        user_headquar.headquar = headquar
                        user_headquar.group = group
                        user_headquar.save()
                    else:
                        if group.id not in group_dist_list:
                            group_dist_list.append(group.id)
                            user.groups.add(group)

                            user_association = UserAssociation()
                            user_association.user = user
                            user_association.association = association
                            user_association.group = group
                            user_association.save()

                            user_enterprise = UserEnterprise()
                            user_enterprise.user = user
                            user_enterprise.enterprise = enterprise
                            user_enterprise.group = group
                            user_enterprise.save()

                            user_headquar = UserHeadquar()
                            user_headquar.user = user
                            user_headquar.headquar = headquar
                            user_headquar.group = group
                            user_headquar.save()

            msg = _('The %(name)s "%(obj)s" was added successfully.') % {
                'name': force_text(self.model._meta.verbose_name),
                'obj': force_text(self.object.username)
            }

            if self.object.id:
                messages.success(self.request, msg)
                log.warning(msg, extra=log_params(self.request))
            return super(SignUpView, self).form_valid(form)

        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.success(self.request, e)
            log.warning(e, extra=log_params(self.request))
            return super(SignUpView, self).form_invalid(form)
