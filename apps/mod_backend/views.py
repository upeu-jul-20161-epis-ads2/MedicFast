from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from apps.utils.decorators import permission_resource_required

# Create your views here.

#@permission_resource_required
def dashboard(request):
    """
    """

    c = {
        'cmi' : 'mod_backend:dashboard',
        'opts': _('Home'),
        'title': _('Backend Home Page.'),
    }
    return render(request, 'mod_backend/base_mod_backend.html', c)