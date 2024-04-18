from django import forms
from .models import PresupuestoMensual, Categoria, GastoMensual


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = PresupuestoMensual
        fields = ['fecha', 'cantidad']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }


class AgregarGastoForm(forms.ModelForm):
    nueva_categoria = forms.CharField(max_length=50, required=False)

    class Meta:
        model = GastoMensual
        fields = ['fecha', 'categoria', 'nueva_categoria', 'descripcion', 'cantidad']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()