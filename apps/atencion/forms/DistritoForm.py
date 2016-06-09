from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize
from ..models import Distrito


class DistritoForm(forms.ModelForm):
    """Class DistritoForm."""
    class Meta:
        model = Distrito
        exclude = ('es_matriculado',)
