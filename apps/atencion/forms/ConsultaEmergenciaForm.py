from django import forms
from ..models import ConsultaEmergencia


class ConsultaEmergenciaForm(forms.ModelForm):
    """Class ConsultaEmergenciaForm."""
    class Meta:
        model = ConsultaEmergencia
        exclude = ('',)
        widgets = {
            'historia': forms.Select(attrs={'class': 'form-control', 'required':'true'})
        }