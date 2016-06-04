from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models import Producto
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize


class ProductoForm(forms.ModelForm):
    """Class ProductoForm."""
    class Meta:
        model = Producto
        exclude = ('',)
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese codigo'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese descripcion'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese stock'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese precio de compra'})}            
