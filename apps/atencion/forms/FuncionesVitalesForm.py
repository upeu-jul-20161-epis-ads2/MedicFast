from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models import FuncionesVitales
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize


class FuncionesVitalesForm(forms.ModelForm):
    """Class FuncionesVitalesForm."""
    class Meta:
        model = FuncionesVitales
        exclude = ('',)
        widgets = {
            'frecuencia_cardiaca': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese frecuencia cardiaca'}),
            'frecuencia_respiratoria': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese frecuencia respiratoria'}),
            'presion_arterial': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese presion arterial'}),
            'temperatura': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese temperatura'}),
            'peso': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese peso'}),
            'talla': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese talla'}),
            'masa_corporal': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese masa corporal'}),
            'diagnostico_mc': forms.TextInput(attrs={'class': 'form-control', 'required':'true'})}
