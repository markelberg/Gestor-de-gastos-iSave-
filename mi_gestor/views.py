import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import PresupuestoForm
from .models import PresupuestoMensual, Categoria, Gasto
from collections import defaultdict
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'POST':
        if 'loginBt' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mi_gestor:home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')

        elif 'signupBt' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('mi_gestor:home')

    return render(request, 'index.html')


@login_required
def home(request):
    presupuestos = PresupuestoMensual.objects.filter(usuario=request.user)
    meses = [presupuesto.mes for presupuesto in presupuestos]
    cantidades = [float(presupuesto.cantidad) for presupuesto in presupuestos]

    gastos_acumulados = []
    for mes in meses:
        gastos_mes = Gasto.objects.filter(usuario=request.user, fecha__month=mes).aggregate(total=Sum('cantidad'))[
            'total']
        gastos_acumulados.append(gastos_mes if gastos_mes else 0)

    diferencia = [p - g for p, g in zip(cantidades, gastos_acumulados)]

    plt.figure(figsize=(10, 6))
    plt.bar(meses, diferencia, color='skyblue')
    plt.xlabel('Mes')
    plt.ylabel('Diferencia (Presupuesto - Gastos acumulados)')
    plt.title('Resumen mensual')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar la gráfica como una imagen en el directorio de medios
    plt.savefig('media/resumen_mensual.png')

    presupuesto_url = '/ingresar-presupuesto/'
    agregar_gastos_url = '/agregar-gastos/'

    return render(request, 'home.html', {'presupuesto_url': presupuesto_url,
                                         'agregar_gastos_url': agregar_gastos_url})


@login_required
def ingresar_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            mes = form.cleaned_data['mes']
            year = form.cleaned_data['year']
            cantidad = form.cleaned_data['cantidad']

            # Verificar si ya existe un presupuesto para este mes y año
            presupuesto_existente = PresupuestoMensual.objects.filter(mes=mes, year=year, usuario=request.user).exists()
            if presupuesto_existente:
                # Actualizar el presupuesto existente
                presupuesto = PresupuestoMensual.objects.get(mes=mes, year=year, usuario=request.user)
                presupuesto.cantidad = cantidad
                presupuesto.save()
            else:
                # Crear un nuevo presupuesto
                presupuesto = PresupuestoMensual(usuario=request.user, mes=mes, year=year, cantidad=cantidad)
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
            categoria_nombre = form.cleaned_data['nueva_categoria']
            categoria_existente = Categoria.objects.filter(nombre=categoria_nombre).exists()

            if categoria_existente:
                categoria = Categoria.objects.get(nombre=categoria_nombre)
            else:
                categoria = Categoria.objects.create(nombre=categoria_nombre)

            gasto = form.save(commit=False)
            gasto.usuario = request.user
            gasto.categoria = categoria
            gasto.save()

            return redirect('home')  # Redirigir a la página de inicio después de guardar el gasto
    else:
        form = AgregarGastoForm()

    return render(request, 'agregar_gastos.html', {'form': form})
