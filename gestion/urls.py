from django.urls import path
from . import views
from .views import login_view, logout_view, register_view

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('mesero/', views.inicio_mesero, name='inicio_mesero'),
    path('mesero/mesas/', views.mesas_mesero, name='mesas_mesero'),
    path('mesero/ordenes/', views.ordenes_mesero, name='ordenes_mesero'),
    path('mesero/menu/', views.menu_mesero, name='menu_mesero'),
    path('mesero/clientes/', views.clientes_mesero, name='clientes_mesero'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),

    path('empleados/', views.empleados, name='empleados'),
    path('empleados/nuevo/', views.empleado_create, name='empleado_create'),
    path('empleados/<int:pk>/editar/', views.empleado_update, name='empleado_update'),
    path('empleados/<int:pk>/eliminar/', views.empleado_delete, name='empleado_delete'),

    path('mesas/', views.mesas, name='mesas'),
    path('mesas/nuevo/', views.mesa_create, name='mesa_create'),
    path('mesas/<int:pk>/editar/', views.mesa_update, name='mesa_update'),
    path('mesas/<int:pk>/eliminar/', views.mesa_delete, name='mesa_delete'),

    path('platos/', views.platos, name='platos'),
    path('platos/nuevo/', views.plato_create, name='plato_create'),
    path('platos/<int:pk>/editar/', views.plato_update, name='plato_update'),
    path('platos/<int:pk>/eliminar/', views.plato_delete, name='plato_delete'),

    path('ordenes/', views.ordenes, name='ordenes'),
    path('ordenes/<int:pk>/detalle/', views.orden_detalles, name='orden_detalles'),

    path('ordenes/nuevo/', views.orden_create, name='orden_create'),
    path('ordenes/<int:pk>/editar/', views.orden_update, name='orden_update'),
    path('ordenes/<int:pk>/eliminar/', views.orden_delete, name='orden_delete'),

    path('ordenes/<int:orden_id>/agregar-plato/', views.agregar_plato_a_orden, name='agregar_plato_a_orden'),

    path('facturas/', views.facturas, name='facturas'),


    path('facturas/orden/<int:orden_id>/crear/', views.factura_create_from_orden, name='factura_create_from_orden'),
    path('facturas/<int:pk>/', views.factura_detail, name='factura_detail'),

    path('facturas/<int:pk>/eliminar/', views.factura_delete, name='factura_delete'),


    path('login/', login_view, name='login'),
    path('registro/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    path('inicio-cajero/', views.inicio_cajero, name='inicio_cajero'),
    path('ordenes-cajero/', views.ordenes_cajero, name='ordenes_cajero'),
    path('facturas-cajero/', views.facturas_cajero, name='facturas_cajero'),
    path('ventas-cajero/', views.ventas_cajero, name='ventas_cajero'),
]
