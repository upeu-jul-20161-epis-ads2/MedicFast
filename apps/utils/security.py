# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Clases para controlar la seguridad de la información en la nube

"""
#from apps.utils.messages import Message
from django.utils.translation import ugettext as _, ungettext
from django.contrib import messages
import datetime
import random

import hashlib

from array import *
from django.shortcuts import redirect
#import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.http import HttpResponse
from django.db import models
from django.utils.encoding import force_text
from django.contrib.admin.utils import NestedObjects, get_deleted_objects
from django.db import transaction, DEFAULT_DB_ALIAS, router
from django.utils.text import capfirst, get_text_list
from django.core.exceptions import ValidationError


def get_dep_objects(instance, using=DEFAULT_DB_ALIAS):
    """
    Find all objects related to ``objs`` that should also be deleted. ``objs``
    must be a homogeneous iterable of objects (e.g. a QuerySet).

    Returns a nested list of strings suitable for display in the
    template with the ``unordered_list`` filter.

    """
    collector = NestedObjects(using=using)
    collector.collect([instance])

    def format_callback(obj):
        no_edit_link = '%s: %s' % (capfirst(force_text(obj._meta.verbose_name)),
                                   force_text(obj))
        return no_edit_link

    def format_callback2(obj):
        no_edit_link = '%s' % (capfirst(force_text(obj._meta.verbose_name)))
        return no_edit_link

    #ver_objs = collector.nested(format_callback)
    objects = collector.nested()
    # print objects

    deps = []

    try:
        for x in objects[1]:
            if type(x) is not list:
                deps.append(x)
    except:
        pass

    # obteniendo mensaje para eliminar

    msg_del = ''

    if deps:
        objs = []
        for p in deps:
            if not 'relationship' in force_text(p._meta.verbose_name):
                objs.append(
                    _(u'<br>%(class_name)s: "%(instance)s"') % {
                        'class_name': capfirst(force_text(p._meta.verbose_name)),
                        'instance': force_text(p) + ' (' + force_text(p.pk) + ')'}
                )
        params = {
            'class_name': capfirst(force_text(instance._meta.verbose_name)),
            'instance': force_text(instance),
            'related_objects': get_text_list(objs, _('and'))}
        msg = _("Deleting %(class_name)s %(instance)s would require deleting the following "
                "protected related objects: %(related_objects)s")
        msgx = _("Deleting the %(object_name)s '%(escaped_object)s' would require deleting the "
                "following protected related objects:")
        #raise ValidationError(force_text(msg), code='deleting_protected', params=params)
        #raise Exception(msg)
        # messages.success(self.request, (', ').join(deps)# )
        msg_del = force_text(msg % params)

        msg_delx = msgx % {
            'object_name': capfirst(force_text(instance._meta.verbose_name)),
            'escaped_object': get_text_list(objs, _('and'))}

    return deps, msg_del


def convert_old_style_list(list_):
    """
        Converts old style lists to the new easier to understand format.

        The old list format looked like:
            ['Item 1', [['Item 1.1', []], ['Item 1.2', []]]

        And it is converted to:
            ['Item 1', ['Item 1.1', 'Item 1.2]]
    """
    if not isinstance(list_, (tuple, list)) or len(list_) != 2:
        return list_, False
    first_item, second_item = list_
    if second_item == []:
            return [first_item], True
    try:
            # see if second item is iterable
        iter(second_item)
    except TypeError:
        return list_, False
    old_style_list = True
    new_second_item = []
    for sublist in second_item:
        item, old_style_list = convert_old_style_list(sublist)
        if not old_style_list:
            break
        new_second_item.extend(item)
    if old_style_list:
        second_item = new_second_item
    return [first_item, second_item], old_style_list


def log_params(request):
    return {
        'path': request.get_full_path(),
        'ip': request.META['REMOTE_ADDR'],
        'user': request.user
    }


class SecurityKey:

    """
            Clase que permite crear llave de seguridad en las url.
    """
    TEXT_KEY = 'lyHyRajh987r.P~CFCcJ[AvFKdz|86'

    # Método para generar las llaves de seguridad
    @staticmethod
    def get_key(id, action_name):
        """
        Genera una llave de seguridad válida durante todo el día %Y-%m-%d

        Entrada::

                id=1
                action_name="user_upd"

        Salida::

                1.dfad09debee34f8e85fccc5adaa2dadb
        """
        key = "%s%s" % (
            SecurityKey.TEXT_KEY, datetime.datetime.now().strftime('%Y-%m-%d'))

        m = hashlib.md5(("%s%s%s" % (id, key, action_name)).encode())
        key = m.hexdigest()

        return u"%s.%s" % (id, key)

    # Método para verificar si la llave es válida
    @staticmethod
    def is_valid_key(request, key_value, action_name):
        """
        Genera una llave de seguridad válida durante todo el día %Y-%m-%d

        Entrada::

                key_value=1.dfad09debee34f8e85fccc5adaa2dadb
                action_name="user_upd"

        Salida::

                1
    """
        key = key_value.split('.')
        _id = key[0]
        valid_key = SecurityKey.get_key(_id, action_name)
        valid = (True if valid_key == key_value else False)
        if not valid:
            #raise Exception(("Acceso denegado. La llave de seguridad es incorrecta."))
            messages.warning(
                request, _('Access denied. The security key is incorrect.'))
            # Message.error(
            # request, ('Acceso denegado. La llave de seguridad es
            # incorrecta.'))
            return False
        # print 'key_value(%s) = valid_key(%s)' % (key_value, valid_key)
        # Message.info(request,('key_value(%s) = valid_key(%s)' % (key_value, valid_key)))
        return _id


class UserToken:

    """
    Clase que permite almacenar y recuperar los permisos a datos de las empresas solicitados por los usuarios.
    """
    @staticmethod
    def set_association_id(request, association_id):
        request.session['association_id'] = association_id

    @staticmethod
    def get_association_id(session):
        return session.get('association_id', False)

    @staticmethod
    def set_enterprise_id(request, enterprise_id):
        request.session['enterprise_id'] = enterprise_id

    @staticmethod
    def get_enterprise_id(session):
        return session.get('enterprise_id', False)

    @staticmethod
    def set_headquar_id(request, headquar_id):
        request.session['headquar_id'] = headquar_id

    @staticmethod
    def get_headquar_id(session):
        return session.get('headquar_id', False)

    @staticmethod
    def set_grupo_id_list(request	, grupo_id_list):
        request.session['grupo_id_list'] = grupo_id_list

    @staticmethod
    def get_grupo_id_list(session):
        return session.get('grupo_id_list', False)


'''
def model_ngettext(obj, n=None):
    """
    Return the appropriate `verbose_name` or `verbose_name_plural` value for
    `obj` depending on the count `n`.

    `obj` may be a `Model` instance, `Model` subclass, or `QuerySet` instance.
    If `obj` is a `QuerySet` instance, `n` is optional and the length of the
    `QuerySet` is used.

    """
    if isinstance(obj, models.query.QuerySet):
        if n is None:
            n = obj.count()
        obj = obj.model
    d = model_format_dict(obj)
    singular, plural = d["verbose_name"], d["verbose_name_plural"]
    return ungettext(singular, plural, n or 0)


def model_format_dict(obj):
    """
    Return a `dict` with keys 'verbose_name' and 'verbose_name_plural',
    typically for use with string formatting.

    `obj` may be a `Model` instance, `Model` subclass, or `QuerySet` instance.

    """
    if isinstance(obj, (models.Model, models.base.ModelBase)):
        opts = obj._meta
    elif isinstance(obj, models.query.QuerySet):
        opts = obj.model._meta
    else:
        opts = obj
    return {
        'verbose_name': force_text(opts.verbose_name),
        'verbose_name_plural': force_text(opts.verbose_name_plural)
    }
'''


class xxxRedirect:

    """
    Clase que permite re-dirigir a un controller, cuaya solicitud se haya realizado con ajax o no

    Antes::

            if request.is_ajax():
                    request.path="/params/locality/index/" #/app/controller_path/action/$params
                    return locality_index(request)
            else:
                    return redirect("/params/locality/index/")


    Ahora solo use (Example)::

            return Redirect.to(request, "/sad/user/index/")
            return Redirect.to_action(request, "index")
    """

    @staticmethod
    def to(request, route, params=None):
        """
        route_list[0] = app
        route_list[1] = controller
        route_list[2] = action
        """
        route = route.strip("/")
        route_list = route.split("/")

        app_name = route_list[0]
        controller_name = ""
        action_name = ""
        if len(route_list) > 1:
            controller_name = route_list[1]
        else:
            raise Exception(("Route no tiene controller"))
        if len(route_list) > 2:
            action_name = route_list[2]

        app = ("apps.%s.views") % app_name

        path = "/%s/%s/" % (app_name, controller_name)
        func = "%s" % (controller_name)
        if action_name:
            path = "/%s/%s/%s/" % (app_name, controller_name, action_name)
            func = "%s_%s" % (controller_name, action_name)

        if request.is_ajax():
            mod = __import__(app, fromlist=[func])
            methodToCall = getattr(mod, func)
            # Message.error(request, "ajax %s"%path)
            request.path = path  # /app/controller_path/action/$params
            return methodToCall(request)
        else:
            # Message.error(request, "noajax %s"%path)
            return redirect(path)

    @staticmethod
    def to_action(request, action_name, params=None):
        """
        route_list[0] = app
        route_list[1] = controller
        route_list[2] = action
        """
        route = request.path
        route = route.strip("/")
        route_list = route.split("/")

        app_name = route_list[0]
        controller_name = ""
        # action_name=""
        if len(route_list) > 1:
            controller_name = route_list[1]
        else:
            raise Exception(("Route no tiene controller"))
        # if len(route_list) > 2:
        # 	action_name = route_list[2]

        app = ("apps.%s.views") % app_name

        path = "/%s/%s/" % (app_name, controller_name)
        func = "%s" % (controller_name)
        if action_name:
            path = "/%s/%s/%s/" % (app_name, controller_name, action_name)
            func = "%s_%s" % (controller_name, action_name)
        # Message.error(request, "path= %s"%path)
        # Message.error(request, "func= %s"%func)
        if request.is_ajax():
            mod = __import__(app, fromlist=[func])
            methodToCall = getattr(mod, func)
            # Message.error(request, "ajax %s"%path)
            request.path = path  # /app/controller_path/action/$params
            return methodToCall(request)
        else:
            # Message.error(request, "noajax %s"%path)
            return redirect(path)
