import datetime
from django import forms
from core import models

class Solicitud_Vacaciones_Form(forms.ModelForm):
    class Meta:
        model = models.VACACIONES
        exclude = ["id_empleado", "cancelado"]
        widgets = {
            'fecha_inicio': forms.DateInput({'type': 'date', 'class': 'CampoFecha'}),
            'fecha_fin': forms.DateInput({'type': 'date', 'class': 'CampoFecha'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'cols': 30,'class': 'CampoMotivo'}),  
        
        }

    def __init__(self, *args, **kwargs):
        self.empleado = kwargs.pop('empleado', None)
        super(Solicitud_Vacaciones_Form, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio <= datetime.date.today(): 
            raise forms.ValidationError("La fecha de inicio debe ser posterior a la fecha actual.")

        if fecha_fin <= fecha_inicio:
            raise forms.ValidationError("La fecha de regreso debe ser posterior a la fecha de inicio.")

        if fecha_inicio and fecha_fin:
            dias_solicitados = (fecha_fin  - fecha_inicio).days - 1
            if dias_solicitados > self.empleado.dias_vacaciones:
                raise forms.ValidationError("No tiene suficientes días de vacaciones disponibles.")
        
        # Verificar solapamientos en las fechas de vacaciones
        vacacionesEmp = models.VACACIONES.objects.filter(id_empleado=self.empleado.id)
        vacaciones_existente = vacacionesEmp.filter(
            fecha_inicio__lte=fecha_fin, 
            fecha_fin__gte=fecha_inicio
        )

        if vacaciones_existente.exists():
            raise forms.ValidationError("Ya existe una solicitud de vacaciones que se solapa con las fechas seleccionadas.")

        return cleaned_data
 

class Solicitud_Permiso_Form(forms.ModelForm):
    TIPO_PERMISO = (
    ("Personal", "Personal"),
    ("Medico", "Medico"),
    ("Emergencia", "Emergencia"),
    )
    tipo = forms.ChoiceField(
        choices=TIPO_PERMISO,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    class Meta:
        model = models.PERMISO
        exclude = ["id_empleado", "cancelado"]
        widgets = {
            'fecha_inicio': forms.DateInput({'type': 'date', 'class': 'CampoFecha'}),
            'fecha_fin': forms.DateInput({'type': 'date', 'class': 'CampoFecha'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'cols': 30,'class': 'CampoMotivo'}),  
            'tipo': forms.Select({"type": "select", "class": "form-select"}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    
    def __init__(self, *args, **kwargs):
        self.empleado = kwargs.pop('empleado', None)
        super(Solicitud_Permiso_Form, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio <= datetime.date.today(): 
            raise forms.ValidationError("La fecha de inicio debe ser posterior a la fecha actual.")

        if fecha_fin <= fecha_inicio:
            raise forms.ValidationError("La fecha de regreso debe ser posterior a la fecha de inicio.")
        
        permisosEmp = models.PERMISO.objects.filter(id_empleado=self.empleado.id)
        vacaciones_existente = permisosEmp.filter(
            fecha_inicio__lte=fecha_fin, 
            fecha_fin__gte=fecha_inicio
        )

        if vacaciones_existente.exists():
            raise forms.ValidationError("Ya existe una solicitud de vacaciones que se solapa con las fechas seleccionadas.")

        return 
 

class Solicitud_Incapacidad_Form(forms.ModelForm):
    class Meta:
        model = models.PERMISO
        exclude = ["id_empleado", "cancelado", "tipo"]
        widgets = {
            'fecha_inicio': forms.DateInput({'type': 'date', 'class': 'CampoFecha'}),
            'fecha_fin': forms.DateInput({'type': 'date', 'class': 'CampoFecha'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'cols': 30,'class': 'CampoMotivo'}),
        }

    
    def __init__(self, *args, **kwargs):
        self.empleado = kwargs.pop('empleado', None)
        super(Solicitud_Incapacidad_Form, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio <= datetime.date.today(): 
            raise forms.ValidationError("La fecha de inicio debe ser posterior a la fecha actual.")

        if fecha_fin <= fecha_inicio:
            raise forms.ValidationError("La fecha de regreso debe ser posterior a la fecha de inicio.")
        
        return 
    

REPORTE = (
    ("Enviado", "Enviado"),
    ("En revision", "En revision"),
    ("Corregido", "Corregido"),
)
SECCION = (
    ("Login", "Inicio de Sesion"),
    ("Permisos", "Permisos"),
    ("Vacaciones", "Vacaciones"),
    ("Nomina", "Nomina"),
    ("Noticias", "Noticias"),
    ("Preguntas", "Preguntas"), 
    ("Datos personales", "Datos personales"),
    ("Otro", "Otro")
)

class ReporteForm(forms.ModelForm):
    class Meta:
        model = models.REPORTE
        fields = ['descripcion', 'seccion', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 30}),
            'seccion': forms.Select(choices=SECCION),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }