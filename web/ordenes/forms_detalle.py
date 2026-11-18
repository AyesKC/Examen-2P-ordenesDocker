from django import forms

class DetalleForm(forms.Form):

    producto = forms.CharField(
        max_length=100
    )

    cantidad = forms.IntegerField()

    precio_unitario = forms.DecimalField(
        max_digits=10,
        decimal_places=2
    )