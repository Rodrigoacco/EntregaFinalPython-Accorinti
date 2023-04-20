from django import forms

class EquipoForm(forms.Form):
    name = forms.CharField(max_length=20)
    n_camada = forms.IntegerField()
