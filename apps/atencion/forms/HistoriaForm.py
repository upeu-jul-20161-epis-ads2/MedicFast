"""Form Historia."""

from django import forms

from ..models import Historia


class HistoriaForm(forms.ModelForm):
    """Class HistoriaForm."""

    class Meta:
        """Meta HistriaForm."""

        model = Historia
        exclude = ('numero', 'estado')
        widgets = {
            'persona': forms.TextInput(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese codigo'}),
            }       