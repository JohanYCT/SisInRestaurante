from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


from django.http import HttpResponseForbidden, HttpResponseRedirect


from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User





from django.shortcuts import get_object_or_404, redirect, render



from .detalle_orden_form import DetalleOrdenForm

from .forms import (
    ClienteForm,
    EmpleadoForm,
    FacturaForm,
    MesaForm,
    OrdenForm,
    PlatoForm,
)
from .models import Cliente, Empleado, Factura, Mesa, Orden, Plato


# Vista para agregar platos a una orden
@login_required
def agregar_plato_a_orden(request, orden_id):
    orden = get_object_or_404(Orden, pk=orden_id)
    if request.method == "POST":
        form = DetalleOrdenForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.orden = orden
            detalle.save()
            return redirect("ordenes")
    else:
        form = DetalleOrdenForm()
    return render(
        request,
        "gestion/agregar_plato_a_orden.html",
        {"form": form, "orden": orden},
    )


@login_required
def inicio(request):
    context = {
        "Total_Clientes": Cliente.objects.count(),
        "Total_Empleados": Empleado.objects.count(),
        "Total_Mesas": Mesa.objects.count(),
        "Total_Platos": Plato.objects.count(),
        "Total_Ordenes": Orden.objects.count(),
        "Total_Facturas": Factura.objects.count(),
    }
    return render(request, "gestion/inicio.html", context)


@login_required
def clientes(request):
    return render(request, "gestion/clientes.html", {"clientes": Cliente.objects.all()})


@login_required
def empleados(request):
    return render(request, "gestion/empleados.html", {"empleados": Empleado.objects.all()})


@login_required
def mesas(request):
    return render(request, "gestion/mesas.html", {"mesas": Mesa.objects.all()})


@login_required
def platos(request):
    return render(request, "gestion/platos.html", {"platos": Plato.objects.all()})


@login_required
def ordenes(request):
    return render(request, "gestion/ordenes.html", {"ordenes": Orden.objects.all()})


@login_required
def orden_detalles(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    detalles = orden.detalles.select_related("plato").all()
    return render(request, "gestion/orden_detalles.html", {"orden": orden, "detalles": detalles})


@login_required
def facturas(request):
    facturas = Factura.objects.all().select_related("orden")
    ordenes = Orden.objects.all()
    return render(request, "gestion/facturas.html", {"facturas": facturas, "ordenes": ordenes})


@login_required
def factura_detail(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    return render(request, "gestion/factura_detail.html", {"factura": factura})


@login_required
def factura_create_from_orden(request, orden_id):
    # Crea la factura a partir de una orden (el usuario solo la selecciona).
    orden = get_object_or_404(Orden, pk=orden_id)

    # Si ya existe factura para esa orden, redirigimos a su vista.
    factura_existente = Factura.objects.filter(orden=orden).first()
    if factura_existente:
        return redirect("factura_detail", pk=factura_existente.pk)

    if request.method == "POST":
        metodo_pago = request.POST.get("metodo_pago")
        subtotal = orden.total
        impuesto = subtotal * Decimal("0.19")  # 19% de IVA
        total_factura = subtotal + impuesto

        factura = Factura.objects.create(
            orden=orden,
            metodo_pago=metodo_pago,
            subtotal=subtotal,
            impuesto=impuesto,
            total_factura=total_factura,
        )

        # Al facturar, la mesa vuelve a estar disponible
        orden.estado_orden = "Facturada"
        orden.save(update_fields=["estado_orden"])

        mesa = orden.mesa
        mesa.estado_mesa = "Disponible"
        mesa.save(update_fields=["estado_mesa"])

        return redirect("factura_detail", pk=factura.pk)


    return render(request, "gestion/factura_form_from_orden.html", {"orden": orden})


@login_required
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("clientes")
    return render(request, "gestion/cliente_form.html", {"form": form})


@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect("clientes")
    return render(request, "gestion/cliente_form.html", {"form": form, "object": cliente})


@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect("clientes")
    return render(request, "gestion/cliente_confirm_delete.html", {"object": cliente})


@login_required
def empleado_create(request):
    form = EmpleadoForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        correo = form.cleaned_data.get("correo")

        # Guardar empleado
        empleado = form.save()

        # Crear/actualizar user auth
        if correo and password:
            UserModel = get_user_model()
            user, created = UserModel.objects.get_or_create(username=correo)
            user.is_staff = True  # permite acceso al panel
            user.set_password(password)
            user.save()

        return redirect("empleados")

    return render(request, "gestion/empleado_form.html", {"form": form})


@login_required
def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        correo = form.cleaned_data.get("correo")

        # Actualizar empleado
        empleado = form.save()

        # Si escribió una nueva contraseña, actualizamos el user auth
        if correo and password:
            UserModel = get_user_model()
            user, _created = UserModel.objects.get_or_create(username=correo)
            user.is_staff = True
            user.set_password(password)
            user.save()

        return redirect("empleados")

    return render(request, "gestion/empleado_form.html", {"form": form, "object": empleado})



@login_required
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        empleado.delete()
        return redirect("empleados")
    return render(request, "gestion/empleado_confirm_delete.html", {"object": empleado})


@login_required
def mesa_create(request):
    form = MesaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("mesas")
    return render(request, "gestion/mesa_form.html", {"form": form})


@login_required
def mesa_update(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    form = MesaForm(request.POST or None, instance=mesa)
    if form.is_valid():
        form.save()
        return redirect("mesas")
    return render(request, "gestion/mesa_form.html", {"form": form, "object": mesa})


@login_required
def mesa_delete(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == "POST":
        mesa.delete()
        return redirect("mesas")
    return render(request, "gestion/mesa_confirm_delete.html", {"object": mesa})


@login_required
def plato_create(request):
    form = PlatoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("platos")
    return render(request, "gestion/plato_form.html", {"form": form})


@login_required
def plato_update(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    form = PlatoForm(request.POST or None, instance=plato)
    if form.is_valid():
        form.save()
        return redirect("platos")
    return render(request, "gestion/plato_form.html", {"form": form, "object": plato})


@login_required
def plato_delete(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        plato.delete()
        return redirect("platos")
    return render(request, "gestion/plato_confirm_delete.html", {"object": plato})


@login_required
def orden_create(request):
    form = OrdenForm(request.POST or None)
    if form.is_valid():
        orden = form.save()
        # Al crear una orden, marcar la mesa como ocupada y no disponible.
        mesa = orden.mesa
        mesa.estado_mesa = "Ocupada"
        mesa.save(update_fields=["estado_mesa"])
        return redirect("ordenes")
    return render(request, "gestion/orden_form.html", {"form": form})


@login_required
def orden_update(request, pk):
    # Las órdenes no se pueden editar. Se mantiene el endpoint para evitar errores por URL.
    return redirect("ordenes")


@login_required
def orden_delete(request, pk):
    # En lugar de eliminar, se cancela la orden y se conserva el registro.
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == "POST":
        orden.estado_orden = "Cancelada"
        orden.save(update_fields=["estado_orden"])

        mesa = orden.mesa
        mesa.estado_mesa = "Disponible"
        mesa.disponible = True
        mesa.save(update_fields=["estado_mesa", "disponible"])

        return redirect("ordenes")

    return render(request, "gestion/orden_confirm_delete.html", {"object": orden})


@login_required
def factura_create(request):
    form = FacturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("facturas")
    return render(request, "gestion/factura_form.html", {"form": form})


@login_required
def factura_delete(request, pk):
    # DIAN: no se permite eliminar ni modificar una factura ya emitida.
    # Endpoint solo para evitar errores por URL.
    return redirect("facturas")


def login_view(request):

    if request.user.is_authenticated:
        return redirect("inicio")

    error = None

    if request.method == "POST":

        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password")

        # ADMIN PRINCIPAL
        if username == "nimda" and password == "nimda321":

            user, _created = User.objects.get_or_create(
                username="nimda",
                defaults={
                    "is_staff": True,
                    "is_superuser": True,
                },
            )

            if not user.check_password(password):
                user.set_password(password)
                user.save(update_fields=["password"])

            login(request, user)

            return redirect("inicio")

        # LOGIN EMPLEADOS
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            try:
                empleado = Empleado.objects.get(correo=username)

                # ADMINISTRADOR
                if empleado.cargo == "Administrador":
                    return redirect("inicio")

                # MESEROS
                elif empleado.cargo in ("Mesero", "Mesera"):
                    return redirect("inicio_mesero")

            except Empleado.DoesNotExist:
                pass

            return redirect("inicio")

        error = "Usuario o contraseña incorrectos"

    return render(
        request,
        "gestion/login.html",
        {"error": error}
    )

@login_required
def inicio_mesero(request):

    mesas = Mesa.objects.all()
    ordenes = Orden.objects.all()
    platos = Plato.objects.all()
    clientes = Cliente.objects.all()

    context = {
        "mesas": mesas,
        "ordenes": ordenes,
        "platos": platos,
        "clientes": clientes,
    }

    return render(
        request,
        "gestion/inicio_mesero.html",
        context
    )
    
# =========================================
# VALIDAR SI ES MESERO
# =========================================

def es_mesero(user):

    try:
        empleado = Empleado.objects.get(correo=user.username)

        return empleado.cargo in ["Mesero", "Mesera"]

    except Empleado.DoesNotExist:
        return False


# =========================================
# MESAS DEL MESERO
# =========================================

@login_required
def mesas_mesero(request):

    if not es_mesero(request.user):
        return redirect("inicio")

    mesas = Mesa.objects.all()

    return render(
        request,
        "gestion/mesas_mesero.html",
        {"mesas": mesas}
    )


# =========================================
# ÓRDENES DEL MESERO
# =========================================

@login_required
def ordenes_mesero(request):

    if not es_mesero(request.user):
        return redirect("inicio")

    ordenes = Orden.objects.all()

    return render(
        request,
        "gestion/ordenes_mesero.html",
        {"ordenes": ordenes}
    )


# =========================================
# MENÚ / PLATOS
# =========================================

@login_required
def menu_mesero(request):

    if not es_mesero(request.user):
        return redirect("inicio")

    platos = Plato.objects.all()

    return render(
        request,
        "gestion/menu_mesero.html",
        {"platos": platos}
    )


# =========================================
# CLIENTES
# =========================================

@login_required
def clientes_mesero(request):

    if not es_mesero(request.user):
        return redirect("inicio")

    clientes = Cliente.objects.all()

    return render(
        request,
        "gestion/clientes_mesero.html",
        {"clientes": clientes}
    )

def register_view(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect("inicio")
    else:
        form = UserCreationForm()

    return render(request, "gestion/registro.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


