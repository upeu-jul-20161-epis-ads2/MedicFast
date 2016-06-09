from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize
from ..models import Persona


class PersonaForm(forms.ModelForm):
    """Class PersonaForm."""
    class Meta:
        model = Persona
        exclude = ('edad','distrito')
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese nombres'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Apellido Materno'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese dni'}),
            'codigo': forms.NumberInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Código'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Fecha de Nacimiento'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'sexo': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Telefono/Celular'}),
            'ocupacion': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'direccion_actual': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Direccion Actual'}),
            'distrito': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese Numero de Contacto'}),
}