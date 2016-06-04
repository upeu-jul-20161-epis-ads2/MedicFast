from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models.atencion import Provincia
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize


def validate_unique_nombre(self):
    """validacion de campo unico"""
    if normalize('NFKD', self).encode('ascii', 'ignore').lower() in list(
            normalize('NFKD', c['nombre']).encode('ascii', 'ignore').lower()
            for c in Provincia.objects.values('nombre')
    ):
        raise forms.ValidationError(
            _(u'%(model_name)s with this %(field_label)s already exists.') % {
                'model_name': capfirst(_('group')),
                'field_label': capfirst(_('nombre')),
            })

class ProvinciaForm(forms.ModelForm):
    """Class ProvinciaForm."""
    class Meta:
        model = Provincia
        exclude = ('usuario',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese nombre'})
            'distrito': forms.Select(attrs={'class': 'form-control', 'required':'true'})

