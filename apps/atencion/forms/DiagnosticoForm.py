from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from ..models import Diagnostico
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms import smtSave, btnCancel, btnReset
from django.utils.text import capfirst, get_text_list
from unicodedata import normalize



class DiagnosticoForm(forms.ModelForm):
    """Class DiagnosticoForm."""
    class Meta:
        model = Diagnostico
        exclude = ('',)
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese codigo'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese nombre'}),
}