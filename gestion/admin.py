from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User

from .models import Cliente, Empleado, Mesa, Plato, Orden, DetalleOrden, Factura

admin.site.register(Cliente)

# El auth.User se gestiona directamente en el admin de Django.
# Así el Administrador puede crear usuarios y asignar contraseña.

admin.site.register(Empleado)
admin.site.register(Mesa)
admin.site.register(Plato)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
admin.site.register(Factura)

# Importar para que el admin pueda mostrar/gestionar grupos y usuarios.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(Group)



