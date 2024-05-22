from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import HttpResponse, HttpResponseForbidden
from core import models 
from users import models as users_models
from RH import forms
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import NominaForm
# Create your views here.

@method_decorator(login_required, name='dispatch')
class Empleados(LoginRequiredMixin, generic.View):
    def get(self, request):
 
        if request.user.groups.filter(name='Personal RH').exists():
            return render(request, "RH/Empleados/empleados.html", {})

        return HttpResponseForbidden("No estás autorizado para ver esta página.")
    
@method_decorator(login_required, name='dispatch')
class Crea_Empleados(LoginRequiredMixin, generic.CreateView):
    model = users_models.CustomUser
    form_class = forms.Crea_Empleado_Form
    template_name = "RH/Empleados/crea_empleados2.html"

    def get_success_url(self):
        return reverse_lazy("RH:crea_empleados2", args=[self.object.id])
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class Crea_Empleados2(LoginRequiredMixin, generic.CreateView):
    model = models.EMPLEADO
    form_class = forms.Crea_Empleado_Form2
    template_name = "RH/Empleados/crea_empleados2.html"
    success_url = reverse_lazy("RH:empleados")

    def get_initial(self):
        initial = super().get_initial()
        user_id = self.kwargs.get('user_id')  
        initial['usuario'] = user_id
        return initial

    def form_valid(self, form):
        form.instance.usuario_id = self.kwargs.get('user_id')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class Edita_Empleados(LoginRequiredMixin, generic.UpdateView):
    model = models.EMPLEADO
    form_class = forms.Crea_Empleado_Form2 
    template_name = "RH/Empleados/edita_empleado.html"
    success_url = reverse_lazy("RH:empleados")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    

@method_decorator(login_required, name='dispatch')
class Edita_Empleados_Busqueda(LoginRequiredMixin, generic.View):
    template_name = "RH/Empleados/edita_empleados_list.html"
    context = {}

    def get(self, request):
        grupo_emp = Group.objects.get(name='Empleados')
        empleados = models.EMPLEADO.objects.filter(usuario__groups=grupo_emp)
        self.context = {
            "empleados" : empleados
        }
        return render(request, self.template_name, self.context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)


class EmpleadoMixin:
    def buscaEmpleado(self, numero_empleado):
        try:
            usuario = users_models.CustomUser.objects.get(numero_empleado=numero_empleado)
            empleado = models.EMPLEADO.objects.get(usuario=usuario)
            return empleado
        except ObjectDoesNotExist:
            return None

@method_decorator(login_required, name='dispatch')
class Edita_Empleados_List(LoginRequiredMixin, EmpleadoMixin, generic.View):
    
    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        
        empleadoAB = request.GET.get('busquedaEmpleado')
        empleado = self.buscaEmpleado(empleadoAB)
        try: 
            usuario = users_models.CustomUser.objects.get(numero_empleado=empleadoAB)
        except ObjectDoesNotExist:
            usuario = None
            
        if empleado:
            return render(request, "RH/Empleados/empleado_busqueda.html", {"empleado": empleado, "usuario": usuario})
        else:
            return HttpResponse('Empleado no encontrado', status=404)

class Empleado_Detalles(LoginRequiredMixin, generic.View):
    template_name = "RH/Empleados/empleado_filter.html"
    context = {}

    def get(self, request, pk):
        usuario = users_models.CustomUser.objects.get(numero_empleado=pk)
        self.context = {
            
            "empleado" : models.EMPLEADO.objects.get(usuario=usuario)
        }
        return render(request, self.template_name, self.context)

@method_decorator(login_required, name='dispatch')
class Elimina_Empleados(LoginRequiredMixin, generic.DeleteView):
    model = users_models.CustomUser
    template_name = "RH/Empleados/empleado_eliminado_confirmacion.html"
    success_url = reverse_lazy("RH:empleados")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)

    
@method_decorator(login_required, name='dispatch')
class Vacaciones_Busqueda(LoginRequiredMixin, generic.View):
    template_name = "RH/Vacaciones/vacaciones_busqueda.html"
    context = {}

    def get(self, request):
        resultados = models.ESTADO_SOLICITUD.objects.filter(id_vacaciones__isnull=False)
        resultados_revision = resultados.filter(estado="En revision")
        vacaciones = [estado.id_vacaciones for estado in resultados_revision]
        self.context = {
            "resultados": resultados_revision,
            "vacaciones": vacaciones
        }
        return render(request, self.template_name, self.context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
    
@method_decorator(login_required, name='dispatch')
class Edita_Vacaciones(LoginRequiredMixin, generic.UpdateView):
    model = models.ESTADO_SOLICITUD
    form_class = forms.EstadoSolicitudForm 
    template_name = "RH/Vacaciones/vacaciones_estado.html"
    success_url = reverse_lazy("RH:vacaciones_busqueda")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)

@login_required
def searchVacaciones(request, *args, **kwargs):
    
    if request.method == 'GET':
        resultados = models.ESTADO_SOLICITUD.objects.filter(id_vacaciones__isnull=False)
        resultados_revision = resultados.filter(estado="En revision")
        vacaciones = [estado.id_vacaciones for estado in resultados_revision] 
        

        vacacionesAB = request.GET.get('busquedaVacacion').lower()
           
        month_mapping = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
        'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
        'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        month_number = str(month_mapping.get(vacacionesAB, 0)) 

        filtered_vacations = []
        filtered_solicitudes = []

        for vacacion in vacaciones:
            if str(vacacion.fecha_inicio.month) == month_number:
                filtered_vacations.append(vacacion)
                filtered_solicitudes.append(models.ESTADO_SOLICITUD.objects.get(id_vacaciones=vacacion.id))
   
        if month_number:
            results = filtered_vacations
            solicitudes = filtered_solicitudes
        else:
            results = models.VACACIONES.objects.none() 

        return render(request, "RH/Vacaciones/vacaciones_filter.html", {"vacaciones": solicitudes})


@method_decorator(login_required, name='dispatch')
class Permisos_Busqueda(LoginRequiredMixin, generic.View):
    template_name = "RH/Permisos/permisos_busqueda.html"
    context = {}

    def get(self, request):
        resultados = models.ESTADO_SOLICITUD.objects.filter(id_permiso__isnull=False)
        resultados_revision = resultados.filter(estado="En revision")

        self.context = {
            "resultados": resultados_revision,
        }
        return render(request, self.template_name, self.context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class Edita_Permisos(LoginRequiredMixin, generic.UpdateView):
    model = models.ESTADO_SOLICITUD
    form_class = forms.EstadoSolicitudForm 
    template_name = "RH/Permisos/permisos_estado.html"
    success_url = reverse_lazy("RH:permisos_busqueda")

@login_required
def searchPermisos(request, *args, **kwargs):
    
    if request.method == 'GET':
        resultados = models.ESTADO_SOLICITUD.objects.filter(id_permiso__isnull=False)
        resultados_revision = resultados.filter(estado="En revision")
        permisos = [estado.id_permiso for estado in resultados_revision] 
        

        permisosAB = request.GET.get('busquedaPermiso').lower()
           
        month_mapping = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
        'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
        'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        month_number = str(month_mapping.get(permisosAB, 0)) 

        filtered_solicitudes = []

        for vacacion in permisos:
            if str(vacacion.fecha_inicio.month) == month_number:
                filtered_solicitudes.append(models.ESTADO_SOLICITUD.objects.get(id_permiso=vacacion.id))
  
        if month_number:
            solicitudes = filtered_solicitudes
        else:
            results = models.PERMISO.objects.none() 

        return render(request, "RH/Permisos/permisos_filter.html", {"vacaciones": solicitudes})
    

@method_decorator(login_required, name='dispatch')
class Noticias(LoginRequiredMixin, generic.View):
    def get(self, request):
 
        if request.user.groups.filter(name='Personal RH').exists():
            return render(request, "RH/Noticias/noticias.html", {})

        return HttpResponseForbidden("No estás autorizado para ver esta página.")
    
@method_decorator(login_required, name='dispatch')
class Crea_Noticias(LoginRequiredMixin, generic.CreateView):
    model = models.NOTICIAS 
    form_class = forms.NoticiasForm
    template_name = "RH/Noticias/noticias_crear.html"
    success_url = reverse_lazy("RH:noticias")
      
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class ListarNoticias(LoginRequiredMixin, generic.View):
    template_name = "RH/Noticias/noticias_listar.html"
    context = {}

    def get(self, request):
        self.context = {
            "noticias" : models.NOTICIAS.objects.all()
        }
        return render(request, self.template_name, self.context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class DetallesNoticia(LoginRequiredMixin, generic.View):
    template_name = "RH/Noticias/noticia_detalle.html"
    context = {}

    def get(self, request, pk):
        self.context = {
            "noticia" : models.NOTICIAS.objects.get(pk=pk)
        }
        return render(request, self.template_name, self.context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class Edita_Noticias(LoginRequiredMixin, generic.UpdateView):
    model = models.NOTICIAS
    form_class = forms.NoticiasForm
    template_name = "RH/Noticias/noticia_editar.html"
    success_url = reverse_lazy("RH:lista_noticias")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class Elimina_Noticia(LoginRequiredMixin, generic.DeleteView):
    model = models.NOTICIAS
    template_name = "RH/Noticias/noticia_eliminar.html"
    success_url = reverse_lazy("RH:noticias")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@login_required
def searchNoticias(request, *args, **kwargs):
    if request.method == 'GET':
        noticiaAB = request.GET.get('busquedaNoticias')
        if noticiaAB:
            noticiasAB = models.NOTICIAS.objects.filter(Q (titulo__icontains=noticiaAB) | Q(contenido__icontains=noticiaAB) )
        else:
            noticiasAB = None
        return render(request, "RH/Noticias/noticias_filter.html", {"noticias": noticiasAB})

@method_decorator(login_required, name='dispatch')
class Preguntas(LoginRequiredMixin, generic.View):
    def get(self, request):
 
        if request.user.groups.filter(name='Personal RH').exists():
            return render(request, "RH/FAQ/faq.html", {})

        return HttpResponseForbidden("No estás autorizado para ver esta página.")

@method_decorator(login_required, name='dispatch')
class Crea_Preguntas(LoginRequiredMixin, generic.CreateView):
    model = models.PREGUNTAS 
    form_class = forms.PreguntasForm
    template_name = "RH/FAQ/faqs_crear.html"
    success_url = reverse_lazy("RH:faqs")
    
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ListarPreguntas(LoginRequiredMixin, generic.View):
    template_name = "RH/FAQ/faqs_listar.html"
    context = {}

    def get(self, request):
        self.context = {
            "preguntas" : models.PREGUNTAS.objects.all()
        }
        return render(request, self.template_name, self.context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class DetallesPregunta(LoginRequiredMixin, generic.View):
    template_name = "RH/FAQ/faq_detalle.html"
    context = {}

    def get(self, request, pk):
        self.context = {
            "pregunta" : models.PREGUNTAS.objects.get(pk=pk)
        }
        return render(request, self.template_name, self.context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class Edita_Preguntas(LoginRequiredMixin, generic.UpdateView):
    model = models.PREGUNTAS
    form_class = forms.PreguntasForm
    template_name = "RH/FAQ/faq_editar.html"
    success_url = reverse_lazy("RH:lista_faqs")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class Elimina_Pregunta(LoginRequiredMixin, generic.DeleteView):
    model = models.PREGUNTAS
    template_name = "RH/FAQ/faq_eliminar.html"
    success_url = reverse_lazy("RH:lista_faqs")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)

@login_required
def searchPreguntas(request, *args, **kwargs):
    if request.method == 'GET':
        preguntaAB = request.GET.get('busquedaPreguntas')
        if preguntaAB:
            preguntasAB = models.PREGUNTAS.objects.filter(pregunta__icontains=preguntaAB)
        else:
            preguntasAB = None
        return render(request, "RH/FAQ/faq_filter.html", {"preguntas": preguntasAB})

@method_decorator(login_required, name='dispatch')
class Incapacidades(LoginRequiredMixin, generic.View):

    def get(self, request):
        
        self.context = {
            'incapacidades' : models.PERMISO.objects.filter(tipo="Incapacidad"), 
        }
        
        if request.user.groups.filter(name='Personal RH').exists():
            return render(request, "RH/Incapacidades/incapacidades.html", self.context)

        return HttpResponseForbidden("No estás autorizado para ver esta página.")

@method_decorator(login_required, name='dispatch')
class Incapacidades_Detalles(LoginRequiredMixin, generic.View):
    template_name = "RH/Incapacidades/incapacidades_detalle.html"
    context = {}
    
    def get(self, request, pk):
        empleado = models.EMPLEADO.objects.get(usuario=request.user)

        self.context = {
           "solicitud": models.PERMISO.objects.get(id=pk),
        }
        return render(request, self.template_name, self.context)

@login_required
def searchIncapacidades(request, *args, **kwargs):
    if request.method == 'GET':
        empleadoAB = request.GET.get('busquedaIncapacidad')
        usuario = users_models.CustomUser.objects.get(numero_empleado=empleadoAB)
        empleado = models.EMPLEADO.objects.get(usuario=usuario)
        if empleadoAB:
            incapacidadesAB = models.PERMISO.objects.filter(id_empleado=empleado.id, tipo="Incapacidad")
        else:
            incapacidadesAB = None
        return render(request, "RH/Incapacidades/incapacidades_busqueda.html", {"incapacidades": incapacidadesAB})
    
def crea_semana_nominas(request):
    grupo_emp = Group.objects.get(name='Empleados')
    empleados = models.EMPLEADO.objects.filter(usuario__groups=grupo_emp)

    if request.method == 'POST':
        all_forms_valid = True
        for empleado in empleados:
            form = NominaForm(request.POST, prefix=str(empleado.id))
            if not form.is_valid():
                all_forms_valid = False
                break

        if all_forms_valid:
            for empleado in empleados:
                form = NominaForm(request.POST, prefix=str(empleado.id))
                if form.is_valid():
                    data = form.cleaned_data
                    fecha_inicio = data['fecha_inicio']
                    salario_diario = data['salario_diario']
                    horas_trabajadas = data['horas_trabajadas']
                    horas_extra = data['horas_extra']
                    deducciones = data['deducciones']

                    nomina = models.NOMINA.objects.create(
                        fecha_inicio=fecha_inicio,
                        fecha_fin=models.NOMINA.get_fecha_fin(fecha_inicio),
                        salario_diario=salario_diario,
                        horas_trabajadas=horas_trabajadas,
                        horas_extra=horas_extra,
                        percepciones=models.NOMINA.get_percepciones(salario_diario, horas_trabajadas, horas_extra),
                        deducciones=deducciones,
                        id_empleado=empleado,
                    )
                    nomina.save()
            return redirect(reverse_lazy('home:home'))
    else:
        forms = []
        for empleado in empleados:
            forms.append((empleado, NominaForm(prefix=str(empleado.id))))

    context = {'forms': forms}
    return render(request, 'RH/Nominas/crea_semana.html', context)

@method_decorator(login_required, name='dispatch')
class Edita_Reportes(LoginRequiredMixin, generic.UpdateView):
    model = models.REPORTE
    form_class = forms.ReporteForm
    template_name = "RH/Reportes/reporte_detalle.html"
    success_url = reverse_lazy("core:reporte_error")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)
        