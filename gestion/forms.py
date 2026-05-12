from decimal import Decimal
from django import forms
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura

BASE_WIDGET = {
    'class': 'form-input',
    'placeholder': '',
}

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={**BASE_WIDGET, 'placeholder': 'Nombre completo'}),
            'telefono': forms.TextInput(attrs={**BASE_WIDGET, 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={**BASE_WIDGET, 'placeholder': 'Correo electrónico'}),
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'cargo', 'telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={**BASE_WIDGET, 'placeholder': 'Nombre completo'}),
            'cargo': forms.Select(attrs={**BASE_WIDGET}),
            'telefono': forms.TextInput(attrs={**BASE_WIDGET, 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={**BASE_WIDGET, 'placeholder': 'Correo electrónico'}),
        }

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero_mesa', 'capacidad', 'estado_mesa']
        widgets = {
            'numero_mesa': forms.NumberInput(attrs={**BASE_WIDGET, 'placeholder': 'Número de mesa'}),
            'capacidad': forms.NumberInput(attrs={**BASE_WIDGET, 'placeholder': 'Capacidad'}),
            'estado_mesa': forms.Select(attrs={**BASE_WIDGET}),
        }

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre_plato', 'descripcion', 'precio', 'categoria', 'disponible']
        widgets = {
            'nombre_plato': forms.TextInput(attrs={**BASE_WIDGET, 'placeholder': 'Nombre del plato'}),
            'descripcion': forms.Textarea(attrs={**BASE_WIDGET, 'placeholder': 'Descripción', 'rows': 4}),
            'precio': forms.NumberInput(attrs={**BASE_WIDGET, 'placeholder': 'Precio'}),
            'categoria': forms.TextInput(attrs={**BASE_WIDGET, 'placeholder': 'Categoría'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'empleado', 'mesa', 'estado_orden']
        widgets = {
            'cliente': forms.Select(attrs={**BASE_WIDGET}),
            'empleado': forms.Select(attrs={**BASE_WIDGET}),
            'mesa': forms.Select(attrs={**BASE_WIDGET}),
            'estado_orden': forms.Select(attrs={**BASE_WIDGET}),
        }

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'metodo_pago']
        widgets = {
            'orden': forms.Select(attrs={**BASE_WIDGET}),
            'metodo_pago': forms.Select(attrs={**BASE_WIDGET}),
        }

    def save(self, commit=True):
        factura = super().save(commit=False)
        if factura.orden:
            factura.subtotal = factura.orden.total
            factura.impuesto = (factura.subtotal * Decimal('0.19')).quantize(Decimal('0.01'))
            factura.total_factura = factura.subtotal + factura.impuesto
        if commit:
            factura.save()
        return factura
