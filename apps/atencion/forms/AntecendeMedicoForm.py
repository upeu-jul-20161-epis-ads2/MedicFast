from django import forms

from ..models import AntecedenteMedico



class AntecedenteMedicoForm(forms.ModelForm):
    """Class ConsultaForm."""
    class Meta:
        model = AntecedenteMedico
        exclude = ('historia',)
        widgets = {
            'antecedente_morbidos': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese antecedentes', 'rows': '2'}),
            'antecedente_ginecoobstetrico': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese enfermedad actual', 'rows': '2'}),
            'antecedente_medicamento': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese examen fisico', 'rows': '2'}),
            'habito': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese examen fisico', 'rows': '2'}),
            'alergia': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese examen fisico', 'rows': '2'}),
            'antecedente_personal_social': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese examen fisico', 'rows': '2'}),
            'atecedente_familiar': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese examen fisico', 'rows': '2'}),
            'inmunizacion': forms.Textarea(attrs={'class': 'form-control', 'required':'true', 'placeholder': 'Ingrese examen fisico', 'rows': '2'}),
        }