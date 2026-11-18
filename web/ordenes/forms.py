from django import forms

class OrdenForm(forms.Form):

    cliente = forms.CharField(
        max_length=100
    )

    estado = forms.CharField(
        max_length=20
    )