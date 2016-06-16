from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
# from ..models import Pais
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize


"""
class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        exclude = ('usuario',)
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese codigo'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese nombre'})
            'departamento': forms.Select(attrs={'class': 'form-control', 'required':'true'})

"""