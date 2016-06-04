# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Tags para mostrar los menús dinámicos
"""
from django import template
from django.template import resolve_variable, Context
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.conf import settings
from apps.utils.security import UserToken
from apps.space.models import Enterprise, Headquar

from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from django.contrib import messages

from apps.sad.menus import Menus

register = template.Library()


@register.simple_tag
def get_info(request):
    """
    Obtiene 

    """
    info = "Backend"
    if UserToken.get_headquar_id(request.session):
        try:
            sede = Headquar.objects.get(
                id=UserToken.get_headquar_id(request.session))
            info = "%s-%s" % (sede.enterprise.name, sede.name)
        except:
            messages.error(
                request, ("Sede no se encuentra en la base de datos."))

    return info


@register.simple_tag
def load_menu(request, module):
    """
    Interfáz del Método para cargar en variables los menús que se mostrará al usuario

    Usage::

            {% load_menu request 'MODULE_KEY' %}

    Definition::

    ('WEB', 'Web informativa'),
    ('VENTAS', 'Ventas'),
    ('BACKEND', 'Backend Manager'),

    Examples::

            {% load_menu request 'BACKEND' %}

    """

    return Menus.load(request, module)


@register.simple_tag
def view_menu(request):
    """
    Interfáz del Método para renderizar el menú

    Usage::

            {% view_menu request %}

    Examples::

            {% view_menu request %}

    """

    return mark_safe(Menus.view(request))
