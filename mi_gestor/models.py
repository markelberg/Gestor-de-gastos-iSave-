from django.db import models
from django.contrib.auth.models import User


class PresupuestoMensual(models.Model):
    mes = models.CharField(max_length=20)
    year = models.IntegerField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Presupuesto de {self.usuario.username} - {self.mes.strftime('%B %Y')}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Gasto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True, default=None)
    descripcion = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Gasto de {self.usuario.username} - {self.descripcion} ({self.costo} €)"
