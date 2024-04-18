import matplotlib.pyplot as plt
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import PresupuestoForm, AgregarGastoForm
from .models import PresupuestoMensual, Categoria, GastoMensual


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')
            print('¡Inicio de sesión exitoso!')
            return redirect('mi_gestor:home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            print('¡Inicio de sesión fallido!')

    return render(request, 'index.html')


@login_required
def home(request):

    mes_actual = datetime.date.today().replace(day=1)

    try:
        presupuesto_mensual = PresupuestoMensual.objects.get(usuario=request.user, fecha=mes_actual)
        presupuesto_mes_actual = presupuesto_mensual.cantidad
    except PresupuestoMensual.DoesNotExist:
        presupuesto_mes_actual = 0

    gastos_mes_actual = GastoMensual.objects.filter(usuario=request.user, fecha__month=mes_actual.month, fecha__year=mes_actual.year).aggregate(total_mes=Sum('cantidad'))
    total_mes_actual = round(gastos_mes_actual['total_mes'], 2) if gastos_mes_actual['total_mes'] else 0

    diferencia = presupuesto_mes_actual - total_mes_actual

    gastos = GastoMensual.objects.filter(usuario=request.user)
    presupuesto_url = '/ingresar_presupuesto/'
    agregar_gastos_url = '/agregar_gastos/'

    return render(request, 'home.html', {
        'presupuesto_url': presupuesto_url,
        'agregar_gastos_url': agregar_gastos_url,
        'gastos': gastos,
        'presupuesto_mes_actual': presupuesto_mes_actual,
        'total_mes_actual': total_mes_actual,
        'diferencia': diferencia
    })


@login_required
def ingresar_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            cantidad = form.cleaned_data['cantidad']

            presupuesto = PresupuestoMensual(fecha=fecha, cantidad=cantidad, usuario=request.user)
            presupuesto.save()

            return redirect('mi_gestor:home')
    else:
        form = PresupuestoForm()

    return render(request, 'ingresar_presupuesto.html', {'form': form})


@login_required
def agregar_gastos(request):
    if request.method == 'POST':
        form = AgregarGastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.usuario = request.user
            gasto.save()

            return redirect('mi_gestor:home')
    else:
        form = AgregarGastoForm()

    return render(request, 'agregar_gastos.html', {'form': form})


@login_required
def eliminar_gasto(request, gasto_id):
    gasto = get_object_or_404(GastoMensual, id=gasto_id)
    if request.method == 'POST':
        gasto.delete()
        return redirect('mi_gestor:home')
    return render(request, 'eliminar_gasto.html', {'gasto': gasto})

