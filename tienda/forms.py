from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import MensajeContacto, Producto, PerfilCliente


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'imagen'
        ]

    def clean_precio(self):
        precio = self.cleaned_data['precio']

        if precio <= 0:
            raise forms.ValidationError(
                _('El precio debe ser mayor a 0')
            )

        return precio


class UserPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
        labels = {
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'email': _('Correo electrónico')
        }


class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        fields = [
            'telefono',
            'direccion',
            'direccion_secundaria',
            'foto'
        ]
        labels = {
            'telefono': _('Número de teléfono'),
            'direccion': _('Dirección principal'),
            'direccion_secundaria': _('Dirección secundaria'),
            'foto': _('Foto de perfil')
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = [
            'nombre',
            'email',
            'telefono',
            'asunto',
            'mensaje'
        ]
        labels = {
            'nombre': _('Nombre'),
            'email': _('Correo electrónico'),
            'telefono': _('Teléfono'),
            'asunto': _('Asunto'),
            'mensaje': _('Mensaje')
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Tu nombre')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('tuemail@correo.com')
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('+56 9 1234 5678')
            }),
            'asunto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Motivo de contacto')
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Escribe tu mensaje'),
                'rows': 5
            })
        }


class CheckoutEnvioForm(forms.Form):
    nombre_completo = forms.CharField(
        label=_('Nombre completo'),
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Nombre y apellido')
        })
    )
    region = forms.CharField(
        label=_('Región'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Ej: Región Metropolitana')
        })
    )
    ciudad = forms.CharField(
        label=_('Ciudad'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Ej: Santiago')
        })
    )
    direccion = forms.CharField(
        label=_('Dirección'),
        max_length=220,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Calle, número, departamento')
        })
    )
    telefono = forms.CharField(
        label=_('Número de teléfono'),
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('+56 9 1234 5678')
        })
    )
    email = forms.EmailField(
        label=_('Correo electrónico'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('correo@ejemplo.com')
        })
    )


class PagoSimuladoForm(forms.Form):
    nombre_titular = forms.CharField(
        label=_('Nombre del titular'),
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Nombre impreso en la tarjeta')
        })
    )
    numero_tarjeta = forms.CharField(
        label=_('Número de tarjeta'),
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('1234 5678 9012 3456'),
            'inputmode': 'numeric'
        })
    )
    fecha_vencimiento = forms.CharField(
        label=_('Fecha de vencimiento'),
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('MM/AA')
        })
    )
    cvv = forms.CharField(
        label=_('CVV'),
        max_length=4,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('123'),
            'inputmode': 'numeric'
        })
    )

    def clean_numero_tarjeta(self):
        numero = self.cleaned_data['numero_tarjeta'].replace(' ', '')

        if not numero.isdigit() or len(numero) < 13 or len(numero) > 16:
            raise forms.ValidationError(
                _('Ingresa un número de tarjeta válido.')
            )

        return numero

    def clean_fecha_vencimiento(self):
        fecha = self.cleaned_data['fecha_vencimiento']

        if len(fecha) != 5 or fecha[2] != '/':
            raise forms.ValidationError(_('Usa el formato MM/AA.'))

        mes, anio = fecha.split('/')

        if not mes.isdigit() or not anio.isdigit():
            raise forms.ValidationError(_('Usa solo números en la fecha.'))

        if int(mes) < 1 or int(mes) > 12:
            raise forms.ValidationError(_('El mes debe estar entre 01 y 12.'))

        return fecha

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']

        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            raise forms.ValidationError(_('Ingresa un CVV válido.'))

        return cvv
