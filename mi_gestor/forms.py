from django import forms
from .models import PresupuestoMensual, Categoria, Gasto


class PresupuestoForm(forms.Form):
    MES_LIST = [
        ('Enero', 'Enero'),
        ('Febrero', 'Febrero'),
        ('Marzo', 'Marzo'),
        ('Abril', 'Abril'),
        ('Mayo', 'Mayo'),
        ('Junio', 'Junio'),
        ('Julio', 'Julio'),
        ('Agosto', 'Agosto'),
        ('Septiembre', 'Septiembre'),
        ('Octubre', 'Octubre'),
        ('Noviembre', 'Noviembre'),
        ('Diciembre', 'Diciembre'),
    ]

    YEAR_LIST = [(str(year), str(year)) for year in range(2024, 2051)]

    mes = forms.ChoiceField(choices=MES_LIST, label='Mes')
    year = forms.ChoiceField(choices=YEAR_LIST, label='Año')
    cantidad = forms.IntegerField(label='Cantidad', required=False)


class AgregarGastoForm(forms.ModelForm):
    nueva_categoria = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Gasto
        fields = ['categoria', 'nueva_categoria', 'descripcion', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
