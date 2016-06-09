# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     home

Descripcion: Implementacion de los controladores de la app home
"""
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.


def saludo_hola_view(request, nombre):
    return HttpResponse('Hola %s' % nombre)


def saludo_hola_template_view(request, nombre):
    messages.warning(request, 'eeeú3')
    c = {
        'nombre': nombre,

    }
    return render(request, 'home/saludo/hola.html', c)


def index(request):
    """
    Muestra la página inical del sistema,
    ie http://localhost:8000/ = http://localhost:8000/home/
    """

    c = {
        'page_module': _('Home'),
        'page_title': _('Home Page.'),
    }
    return render(request, 'home/index_principal.html', c)
