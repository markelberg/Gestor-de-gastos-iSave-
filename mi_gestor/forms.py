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
    
    def clean(self):
        
        cleaned_data = super().clean()
        nueva_categoria = cleaned_data.get('nueva_categoria')
        if nueva_categoria:
            categoria_nueva, _ = Categoria.objects.get_or_create(nombre=nueva_categoria)
            cleaned_data['categoria'] = categoria_nueva
        return cleaned_data