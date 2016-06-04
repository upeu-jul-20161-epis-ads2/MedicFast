from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models.atencion import Historia
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize


def validate_unique_nombre(self):
    """validacion de campo unico"""
    if normalize('NFKD', self).encode('ascii', 'ignore').lower() in list(
            normalize('NFKD', c['numero']).encode('ascii', 'ignore').lower()
            for c in Distrito.objects.values('numero')
    ):
        raise forms.ValidationError(
            _(u'%(model_name)s with this %(field_label)s already exists.') % {
                'model_name': capfirst(_('group')),
                'field_label': capfirst(_('numero')),
            })

class HistoriaForm(forms.ModelForm):
    """Class HistoriaForm."""
    class Meta:
        model = Historia
        exclude = ('',)
        widgets = {
            'estado': forms.TextInput(attrs={'class': 'form-control', 'required':'true'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese nombres'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Apellido Materno'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese dni'}),
            'fecha_nacimiento': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese fecha de nacimiento'}),
            'estado_civil': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese estado civil'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese sexo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese telefono'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese ocupacion'}),
            'direccion_actual': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese direccion actual...'}),
            'pais_procedencia': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'atencion': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'laboratorio': forms.Select(attrs={'class': 'form-control', 'required':'true'})



