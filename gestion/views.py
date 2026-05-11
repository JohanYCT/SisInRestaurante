from django.shortcuts import render, redirect
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    context = {
        'Total_Clientes': Cliente.objects.count(),
        'Total_Empleados': Empleado.objects.count(),
        'Total_Mesas': Mesa.objects.count(),
        'Total_Platos': Plato.objects.count(),
        'Total_Ordenes': Orden.objects.count(),
        'Total_Facturas': Factura.objects.count(),
    }
    return render(request, 'Gestion/inicio.html', context)

@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'Gestion/clientes.html', {'clientes': clientes})

@login_required
def empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'Gestion/empleados.html', {'empleados': empleados})

@login_required
def mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'Gestion/mesas.html', {'mesas': mesas})

@login_required
def platos(request):
    platos = Plato.objects.all()
    return render(request, 'Gestion/platos.html', {'platos': platos})

@login_required
def ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'Gestion/ordenes.html', {'ordenes': ordenes})

@login_required
def facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'Gestion/facturas.html', {'facturas': facturas})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'gestion/login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'gestion/login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('/login/')