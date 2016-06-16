from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models import Tratamiento
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize

class TratamientoForm(forms.ModelForm):
    """Class TratamientoForm."""
    class Meta:
        model = Tratamiento
        exclude = ('fecha',)
        widgets = {
            'recomendacion': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese recomendacion'}),
            'diagnostico': forms.Select(attrs={'class': 'form-control', 'required':'true'}),
            'detalle': forms.Select(attrs={'class': 'form-control'})
        }
