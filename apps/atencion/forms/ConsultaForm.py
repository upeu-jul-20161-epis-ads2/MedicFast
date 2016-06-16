from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models import Consulta
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize


class ConsultaForm(forms.ModelForm):
    """Class ConsultaForm."""
    class Meta:
        model = Consulta
        exclude = ('usuario', 'historia', 'estado', 'hecho')
        widgets = {
            'antecedentes': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese antecedentes', 'rows': '2'}),
            'enfermedad_actual': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese enfermedad actual', 'rows': '2'}),
            'examen_fisico': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese examen fisico', 'rows': '2'}),
            'funciones_vitales': forms.Select(attrs={'class': 'form-control', 'required':'true', 'rows': '2'}),
            'tratamiento': forms.Select(attrs={'class': 'form-control', 'required':'true', 'rows': '2'}),
        }