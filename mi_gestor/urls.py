from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'mi_gestor'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('ingresar_presupuesto/', views.ingresar_presupuesto, name='ingresar_presupuesto'),
    path('agregar_gasto/', views.agregar_gasto, name='agregar_gasto'),
    path('eliminar_gasto/<int:gasto_id>/', views.eliminar_gasto, name='eliminar_gasto'),
    path('meses_previos/', views.meses_previos, name='meses_previos'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)