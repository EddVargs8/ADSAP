import datetime
from django import forms
from core import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group
from django.db import transaction

User = get_user_model()


class Crea_Empleado_Form(UserCreationForm):
    numero_empleado = forms.CharField(required=True)
    email = forms.EmailField(required=True, help_text="Requerido. 254 caracteres o menos. Debe ser una dirección de correo electrónico válida.")
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select,  # Usar Select para una única selección
        help_text="Seleccione un grupo."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('numero_empleado', 'email', 'groups',)

    def save(self, commit=True):
        with transaction.atomic():
            user = super().save(commit=False)
            user.numero_empleado = self.cleaned_data['numero_empleado']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
                user.groups.set([self.cleaned_data['groups']])
        return user

class Crea_Empleado_Form2(forms.ModelForm):
    class Meta:
        model = models.EMPLEADO
        exclude = [
            "usuario",
            "fecha_ingreso",

        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_casa': forms.TextInput(attrs={'class': 'form-control'}),
            'colonia': forms.TextInput(attrs={'class': 'form-control'}),
            'cp': forms.NumberInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control'}),
            'nss': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'dias_vacaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(choices=(("M", "Masculino"), ("F", "Femenino")), attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            #'usuario': forms.Select(attrs={'class': 'form-control'}),
            'id_empresa': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(Crea_Empleado_Form2, self).__init__(*args, **kwargs)
        self.fields['area'].queryset = models.AREA.objects.all()
        #self.fields['usuario'].queryset = CustomUser.objects.all()
        self.fields['id_empresa'].queryset = models.EMPRESA.objects.all()


class EstadoSolicitudForm(forms.ModelForm):
    class Meta:
        model = models.ESTADO_SOLICITUD
        fields = ['estado', 'comentarios_admin'] 

        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'comentarios_admin': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EstadoSolicitudPermisoForm(forms.ModelForm):
    class Meta:
        model = models.ESTADO_SOLICITUD
        fields = ['estado', 'comentarios_admin'] 

        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'comentarios_admin': forms.Textarea(attrs={'class': 'form-control'}),
        }