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
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={**BASE_WIDGET, 'placeholder': 'Contraseña (para login)'}),
        help_text='Deja vacío para no cambiar la contraseña al editar. En la creación se recomienda llenarla.',
    )

    def clean(self):
        cleaned_data = super().clean()
        # Validación simple para evitar correos vacíos
        correo = cleaned_data.get('correo')
        if correo:
            cleaned_data['correo'] = correo.strip().lower()
        return cleaned_data


    class Meta:
        model = Empleado
        fields = ['nombre', 'cargo', 'telefono', 'correo', 'password']
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
        # estado_orden debe quedar por defecto (ej: 'Activa') al crear una orden
        fields = ['cliente', 'empleado', 'mesa']
        widgets = {
            'cliente': forms.Select(attrs={**BASE_WIDGET}),
            'empleado': forms.Select(attrs={**BASE_WIDGET}),
            'mesa': forms.Select(attrs={**BASE_WIDGET}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar mesas disponibles para evitar asignar mesas ocupadas.
        self.fields['mesa'].queryset = Mesa.objects.filter(estado_mesa='Disponible')





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

