from django.urls import path
from . import views
from .views import login_view, logout_view

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('clientes/', views.clientes, name='clientes'), 
    path('empleados/', views.empleados, name='empleados'),
    path('mesas/', views.mesas, name='mesas'),
    path('platos/', views.platos, name='platos'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('facturas/', views.facturas, name='facturas'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
