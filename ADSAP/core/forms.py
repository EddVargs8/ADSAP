from django import forms
from core import models

class Solicitud_Vacaciones_Form(forms.ModelForm):
    class Meta:
        model = models.VACACIONES
        exclude = ["id_empleado"]
        widgets = {
            'fecha_inicio': forms.DateInput({'type': 'date'}),
            'fecha_fin': forms.DateInput({'type': 'date'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'cols': 30}),  
        }

    def __init__(self, *args, **kwargs):
        self.empleado = kwargs.pop('empleado', None)
        super(Solicitud_Vacaciones_Form, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            dias_solicitados = (fecha_fin - fecha_inicio).days + 1
            if dias_solicitados > self.empleado.dias_vacaciones:
                raise forms.ValidationError("No tiene suficientes días de vacaciones disponibles.")
        
        return cleaned_data
 