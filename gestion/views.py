from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura
from .forms import ClienteForm, EmpleadoForm, MesaForm, PlatoForm, OrdenForm, FacturaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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
    return render(request, 'gestion/inicio.html', context)

@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})

@login_required
def empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})

@login_required
def mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesas.html', {'mesas': mesas})

@login_required
def platos(request):
    platos = Plato.objects.all()
    return render(request, 'gestion/platos.html', {'platos': platos})

@login_required
def ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'gestion/ordenes.html', {'ordenes': ordenes})

@login_required
def facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'gestion/facturas.html', {'facturas': facturas})




@login_required
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clientes')
    return render(request, 'gestion/cliente_form.html', {'form': form})


@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect('clientes')
    return render(request, 'gestion/cliente_form.html', {'form': form, 'object': cliente})


@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')
    return render(request, 'gestion/cliente_confirm_delete.html', {'object': cliente})


@login_required
def empleado_create(request):
    form = EmpleadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('empleados')
    return render(request, 'gestion/empleado_form.html', {'form': form})


@login_required
def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if form.is_valid():
        form.save()
        return redirect('empleados')
    return render(request, 'gestion/empleado_form.html', {'form': form, 'object': empleado})


@login_required
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados')
    return render(request, 'gestion/empleado_confirm_delete.html', {'object': empleado})


@login_required
def mesa_create(request):
    form = MesaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mesas')
    return render(request, 'gestion/mesa_form.html', {'form': form})


@login_required
def mesa_update(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    form = MesaForm(request.POST or None, instance=mesa)
    if form.is_valid():
        form.save()
        return redirect('mesas')
    return render(request, 'gestion/mesa_form.html', {'form': form, 'object': mesa})


@login_required
def mesa_delete(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        return redirect('mesas')
    return render(request, 'gestion/mesa_confirm_delete.html', {'object': mesa})


@login_required
def plato_create(request):
    form = PlatoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('platos')
    return render(request, 'gestion/plato_form.html', {'form': form})


@login_required
def plato_update(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    form = PlatoForm(request.POST or None, instance=plato)
    if form.is_valid():
        form.save()
        return redirect('platos')
    return render(request, 'gestion/plato_form.html', {'form': form, 'object': plato})


@login_required
def plato_delete(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.delete()
        return redirect('platos')
    return render(request, 'gestion/plato_confirm_delete.html', {'object': plato})


@login_required
def orden_create(request):
    form = OrdenForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('ordenes')
    return render(request, 'gestion/orden_form.html', {'form': form})


@login_required
def orden_update(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    form = OrdenForm(request.POST or None, instance=orden)
    if form.is_valid():
        form.save()
        return redirect('ordenes')
    return render(request, 'gestion/orden_form.html', {'form': form, 'object': orden})


@login_required
def orden_delete(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.delete()
        return redirect('ordenes')
    return render(request, 'gestion/orden_confirm_delete.html', {'object': orden})


@login_required
def factura_create(request):
    form = FacturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('facturas')
    return render(request, 'gestion/factura_form.html', {'form': form})


@login_required
def factura_update(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    form = FacturaForm(request.POST or None, instance=factura)
    if form.is_valid():
        form.save()
        return redirect('facturas')
    return render(request, 'gestion/factura_form.html', {'form': form, 'object': factura})


@login_required
def factura_delete(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        factura.delete()
        return redirect('facturas')
    return render(request, 'gestion/factura_confirm_delete.html', {'object': factura})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        error = 'Usuario o contraseña incorrectos'

    return render(request, 'gestion/login.html', {'error': error})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()

    return render(request, 'gestion/registro.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')