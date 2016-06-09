from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models import Laboratorio
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize


class LaboratorioForm(forms.ModelForm):
    """Class LaboratorioForm."""
    class Meta:
        model = Laboratorio
        exclude = ('',)
        widgets = {
            'hemoglobina': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese hemoglobina'}),
            'endocritos': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese frecuencia endocritos'}),
            'globulos_rojos': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese globulos rojos'}),
            'globulos_blancos': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese globulos blancos'}),
            'tipo_sangre': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese tipo de sangre'})}
