from core.models import EMPLEADO

def datos_empleado(request):
    if request.user.is_authenticated:
            empleado = EMPLEADO.objects.get(usuario=request.user)
            return {
            'empleado_id': empleado.id,
            'empleado_nombre': empleado.nombre,
            'empleado_apellido_paterno': empleado.apellido_paterno,
            'empleado_apellido_materno': empleado.apellido_materno,
            'empleado_empresa': empleado.id_empresa.nombre,
            }
    else:
        return {}
        
