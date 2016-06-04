# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Decorador para validar los permisos de los usuarios

"""
from django.utils.translation import ugettext as _  # , ungettext
from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import messages
from django.template.context import RequestContext
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
#from django.utils.decorators import method_decorator
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve
from django.http import HttpResponseRedirect, Http404
from django.conf import settings

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import ValidationError


def is_admin(view_func):
    '''
    Verifica si es admin o no
    Usage::

        from apps.sad.decorators import is_admin

        @is_admin
        def function_name(request):

    Example::

        @is_admin
        def locality_index(request, field='name', value='None', order='-id'):
            return render_to_response('params/locality/index.html', c, context_instance = RequestContext(request))
    '''
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse(u'<h3>Necesitas privilegios de aministrador para realizar esta acción</h3>')
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func


def permission_resource_required(function=None, template_name='mod_backend/base_mod_backend.html', login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Verifica si el usuario tiene permiso para acceder al recurso actual (request.path)

    Usage::

        from apps.sad.decorators import permission_resource_required

        @permission_resource_required
        def function_name(request):

        @permission_resource_required(template_name='denied_mod_ventas.html')
        def function_name(request):

    Example::

        @permission_resource_required
        def user_index(request, field='username', value='None', order='-id'):
            ...
            render_to_response('sad/user/index.html', c, context_instance = RequestContext(request))
    """
    actual_decorator = permission_resource_required_decorator(
        template_name=template_name,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def permission_resource_required_decorator(template_name='mod_backend/base_mod_backend.html', login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Implementa el docorador permission_resource_required
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            from django.utils.encoding import force_str
            from django.utils.six.moves.urllib.parse import urlparse
            from django.shortcuts import resolve_url

            path = request.build_absolute_uri()
                # urlparse chokes on lazy objects in Python 3, force to str
            resolved_login_url = force_str(
                resolve_url(login_url or settings.LOGIN_URL))
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
               (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login

            if not request.user.is_authenticated():
                messages.warning(request, _(u'Authentication is required'))
                # raise PermissionDenied  # 403.html
                # return render_to_response('403.html', {'': ''},
                # context_instance=RequestContext(request))

                # https://github.com/django/django/blob/master/django/contrib/auth/decorators.py
                return redirect_to_login(path, resolved_login_url, redirect_field_name)

            #path += '&PermissionDenied'
            #print path
            permiso = ''
            recurso = '/'

            try:
                path_c = request.path.strip(
                    '/')  # request.get_full_path().strip('/') #'/apps/controller/action/' to 'apps/controller/action'

            except Exception as e:
                raise Exception(e)
            # current_url = resolve(request.path_info).url_name
            # print 'current_url=%s' % current_url

            path_list = path_c.split('/')
            permiso = '%s.' % (path_list[0])
            recurso = '/%s/' % (path_list[0])
            if not isinstance(permiso, (list, tuple)):
                perms = (permiso,)
            else:
                perms = permiso

            if not request.user.has_perms(perms) and len(path_list) > 1:
                permiso = '%s.%s' % (path_list[0], path_list[1])
                recurso = '/%s/%s/' % (path_list[0], path_list[1])

            if not isinstance(permiso, (list, tuple)):
                perms = (permiso,)
            else:
                perms = permiso
            if not request.user.has_perms(perms) and len(path_list) > 2:
                permiso = '%s.%s_%s' % (
                    path_list[0], path_list[1], path_list[2])
                recurso = '/%s/%s/%s/' % (
                    path_list[0], path_list[1], path_list[2])

            if not isinstance(permiso, (list, tuple)):
                perms = (permiso,)
            else:
                perms = permiso
            if request.user.has_perms(perms):
                return view_func(request, *args, **kwargs)
            else:

                messages.warning(
                    request, _('Permission denied. You don\'t have permission to %s.') % (recurso) )
                #raise PermissionDenied
                # return HttpResponseRedirect('/%s'%path_c) # bucle
                # return render_to_response(template_name, {'': ''},
                # context_instance=RequestContext(request))
                # return render(request, template_name)
                # if settings.DEBUG:
                #    raise Http404((
                #                  'Tu no posees permisos para acceder '
                #                  'a %(route)s') % {'route': recurso})
                #raise PermissionDenied
                # return HttpResponseForbidden('You have no permission to do this!')
                return render(request, template_name)
                # return redirect_to_login(path, resolved_login_url,
                # redirect_field_name)

                # return view_func(request, *args, **kwargs)

                #raise ValidationError(
                #    ('Tu no posees permisos para acceder a <b>%(route)s</b>') % {'route': recurso})

        return _wrapped_view
    return decorator
