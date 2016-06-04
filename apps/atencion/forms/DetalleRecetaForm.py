from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models.atencion import DetalleReceta
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize


class DetalleRecetaForm(forms.ModelForm):
    """Class DetalleRecetaForm."""
    class Meta:
        model = DetalleReceta
        exclude = ('',)
        widgets = {
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese precio de venta'}),
            'producto': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese cantidad'}),
            'presentacion': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese dosis'}),
            'periodo': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese periodo'}),
            