from django.forms import IntegerField
from django.shortcuts import redirect, render
from core import models
from core import forms
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.urls import reverse_lazy
from django.db.models import F 
from django.db.models.functions import ExtractMonth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import date 


@method_decorator(login_required, name='dispatch')
class Preguntas(LoginRequiredMixin, generic.View):
    template_name = "faq.html"
    context = {}

    def get(self, request):
        self.context = {
            "preguntas": models.PREGUNTAS.objects.all()
        }

        return render(request, self.template_name, self.context)

@login_required
def searchPreguntas(request, *args, **kwargs):
    if request.method == 'GET':
        preguntaAB = request.GET.get('busqueda')
        if preguntaAB:
            preguntasAB = models.PREGUNTAS.objects.filter(pregunta__icontains=preguntaAB)
        else:
            preguntasAB = None
        return render(request, "faq_filter.html", {"preguntasAB": preguntasAB})


@method_decorator(login_required, name='dispatch')
class Noticias(LoginRequiredMixin, generic.View):
    template_name = "noticia.html"
    context = {}

    def get(self, request):
        self.context = {
            "noticias": models.NOTICIAS.objects.all()
        }

        return render(request, self.template_name, self.context)

@login_required
def searchNoticias(request, *args, **kwargs):
    if request.method == 'GET':
        noticiaAB = request.GET.get('busquedaNoticia')
        if noticiaAB:
            noticiasAB = models.NOTICIAS.objects.filter(Q (titulo__icontains=noticiaAB) | Q(contenido__icontains=noticiaAB) )
        else:
            noticiasAB = None
        return render(request, "noticia_filter.html", {"noticiasAB": noticiasAB})
    
@method_decorator(login_required, name='dispatch')
class Datos_Personales(LoginRequiredMixin, generic.View):
    template_name = "datos_personales.html"
    context = {}

    def get(self, request):
        self.context = {
            "empleado": models.EMPLEADO.objects.get(usuario=request.user)
        }

        return render(request, self.template_name, self.context)
    
@method_decorator(login_required, name='dispatch')
class Vacaciones(LoginRequiredMixin, generic.View):
    template_name = "vacaciones/vacaciones.html"
    context = {}

    def get(self, request):
        empleado = models.EMPLEADO.objects.get(usuario=request.user)

        self.context = {
            "empleado": models.EMPLEADO.objects.get(usuario=request.user),
            "solicitudes": models.VACACIONES.objects.filter(id_empleado=empleado.id),
            "dias_solicitados": models.VACACIONES.dias_solicitados
        }

        return render(request, self.template_name, self.context)

@method_decorator(login_required, name='dispatch')
class Vacaciones_Confirmacion(LoginRequiredMixin, generic.View):
    template_name = "vacaciones/vacaciones_confirmacion.html"
    context = {}

    def get(self, request):
        self.context = {
            
        }

        return render(request, self.template_name, self.context)

@login_required
def Vacaciones_Form(request):
    empleado = models.EMPLEADO.objects.get(usuario=request.user)  # Asumiendo que cada usuario está vinculado a un empleado

    if request.method == 'POST':
        form = forms.Solicitud_Vacaciones_Form(request.POST, empleado=empleado)
        if form.is_valid():
            # Guardar la instancia del formulario, pero no incluir aún el empleado en el modelo
            vacaciones = form.save(commit=False)
            vacaciones.id_empleado = empleado
            vacaciones.save()

            # Calcular los días solicitados
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            dias_solicitados = (fecha_fin - fecha_inicio).days 

            # Actualizar los días de vacaciones del empleado
            empleado.dias_vacaciones = F('dias_vacaciones') - dias_solicitados
            empleado.save()

            return redirect('core:vacaciones_confirmacion')
    else:
        form = forms.Solicitud_Vacaciones_Form(empleado=empleado)

    return render(request, 'vacaciones/form_vacaciones.html', {'form': form})
    
@method_decorator(login_required, name='dispatch')
class Vacaciones_Estado(LoginRequiredMixin, generic.View):
    template_name = "vacaciones/vacaciones_estado.html"
    context = {}

    def get(self, request, pk):
        self.context = {
            "estado_solicitud": models.ESTADO_SOLICITUD.objects.get(id_vacaciones=pk),
            "solicitud": models.VACACIONES.objects.get(id=pk),
            "empleado": models.EMPLEADO.objects.get(usuario=request.user)
        }
        return render(request, self.template_name, self.context)

@method_decorator(login_required, name='dispatch')
class Vacaciones_Eliminacion(LoginRequiredMixin, generic.DeleteView):
    template_name = "vacaciones/vacaciones_eliminacion.html"
    model = models.VACACIONES
    success_url = reverse_lazy('core:vacaciones')
    
    def get(self, request, pk):
        self.context = {
            "estado_solicitud": models.ESTADO_SOLICITUD.objects.get(id_vacaciones=pk),
            "solicitud": models.VACACIONES.objects.get(id=pk),
            "empleado": models.EMPLEADO.objects.get(usuario=request.user),

        }
        return render(request, self.template_name, self.context)
    
@login_required
def searchVacaciones(request, *args, **kwargs):
    
    if request.method == 'GET':
        vacacionesAB = request.GET.get('busquedaVacaciones').lower()
        empleado = models.EMPLEADO.objects.get(usuario=request.user)
        VacacionesEmp = models.VACACIONES.objects.filter(id_empleado=empleado.id)

        month_mapping = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
        'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
        'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        month_number ="0" + str(month_mapping.get(vacacionesAB, 0)) 

        if month_number:
            results = VacacionesEmp.filter(fecha_inicio__month=month_number)
        else:
            results = models.VACACIONES.objects.none() 
        return render(request, "vacaciones/vacaciones_filter.html", {"vacaciones": results})


@method_decorator(login_required, name='dispatch')
class Permisos(LoginRequiredMixin, generic.View):
    template_name = "permisos/permisos.html"
    context = {}

    def get(self, request):
        empleado = models.EMPLEADO.objects.get(usuario=request.user)
        
        self.context = {
            "empleado": empleado,
            "solicitudes": models.PERMISO.objects.filter(id_empleado=empleado.id),
            "dias_solicitados": models.PERMISO.dias_solicitados
        }

        return render(request, self.template_name, self.context)
    

@login_required
def Permisos_Form(request):
    empleado = models.EMPLEADO.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = forms.Solicitud_Permiso_Form(request.POST, empleado=empleado)
        if form.is_valid():
            permiso = form.save(commit=False)
            permiso.id_empleado = empleado
            permiso.save()

            return redirect('core:permisos_confirmacion')
    else:
        form = forms.Solicitud_Permiso_Form(empleado=empleado)

    return render(request, 'permisos/form_permisos.html', {'form': form})
    
@method_decorator(login_required, name='dispatch')
class Permisos_Estado(LoginRequiredMixin, generic.View):
    template_name = "permisos/permisos_estado.html"
    context = {}

    def get(self, request, pk):
        self.context = {
            "estado_solicitud": models.ESTADO_SOLICITUD.objects.get(id_permiso=pk),
            "solicitud": models.PERMISO.objects.get(id=pk),
            "empleado": models.EMPLEADO.objects.get(usuario=request.user)
        }
        return render(request, self.template_name, self.context)
    
@method_decorator(login_required, name='dispatch')
class Permisos_Eliminacion(LoginRequiredMixin, generic.DeleteView):
    template_name = "permisos/permisos_eliminacion.html"
    model = models.PERMISO
    success_url = reverse_lazy('core:permisos')
    
    
    def get(self, request, pk):
        self.context = {
            "estado_solicitud": models.ESTADO_SOLICITUD.objects.get(id_permiso=pk),
            "solicitud": models.PERMISO.objects.get(id=pk),
            "empleado": models.EMPLEADO.objects.get(usuario=request.user),

        }
        return render(request, self.template_name, self.context)
    
@method_decorator(login_required, name='dispatch')
class Permisos_Confirmacion(LoginRequiredMixin, generic.View):
    template_name = "permisos/permisos_confirmacion.html"
    context = {}

    def get(self, request):
        self.context = {
            
        }

        return render(request, self.template_name, self.context)
    
@login_required
def searchPermisos(request, *args, **kwargs):
    if request.method == 'GET':
        permisoAB = request.GET.get('busquedaPermisos').lower()
        empleado = models.EMPLEADO.objects.get(usuario=request.user)
        permisosEmp = models.PERMISO.objects.filter(id_empleado=empleado.id)
        
        month_mapping = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
        'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
        'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        month_number ="0" + str(month_mapping.get(permisoAB, 0)) 

        if month_number:
            results = permisosEmp.filter(fecha_inicio__month=month_number)
        else:
            results = models.PERMISO.objects.none() 
        
        return render(request, "permisos/permisos_filter.html", {"permisos": results})
    

@method_decorator(login_required, name='dispatch')
class Incapacidades(LoginRequiredMixin, generic.View):
    template_name = "incapacidades/incapacidades.html"
    context = {}

    def get(self, request):
        empleado = models.EMPLEADO.objects.get(usuario=request.user)
        
        self.context = {
            "empleado": empleado,
            "solicitudes": models.PERMISO.objects.filter( Q(id_empleado=empleado.id) & Q(tipo="Incapacidad")),
            "dias_solicitados": models.PERMISO.dias_solicitados
        }

        return render(request, self.template_name, self.context)
    
@method_decorator(login_required, name='dispatch')
class Incapacidades_Detalles(LoginRequiredMixin, generic.View):
    template_name = "incapacidades/incapacidades_detalles.html"
    context = {}
    
    def get(self, request, pk):
        empleado = models.EMPLEADO.objects.get(usuario=request.user)

        self.context = {
           "solicitud": models.PERMISO.objects.get(id=pk),
        }
        return render(request, self.template_name, self.context)
    
@login_required
def Incapacidades_Form(request):
    empleado = models.EMPLEADO.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = forms.Solicitud_Incapacidad_Form(request.POST, request.FILES, empleado=empleado)
        if form.is_valid():
            permiso = form.save(commit=False)
            permiso.id_empleado = empleado
            permiso.tipo = "Incapacidad"
            permiso.save()

            return redirect('core:incapacidades')
    else:
        form = forms.Solicitud_Incapacidad_Form(empleado=empleado)

    return render(request, 'incapacidades/incapacidades_crea.html', {'form': form})

@login_required
def searchIncapacidades(request, *args, **kwargs):
    if request.method == 'GET':
        incapacidadAB = request.GET.get('busquedaIncapacidades').lower()
        empleado = models.EMPLEADO.objects.get(usuario=request.user)
        incapacidades = models.PERMISO.objects.filter(tipo="Incapacidad")
        incapacidadesEmp = incapacidades.filter(id_empleado=empleado.id)
        
        month_mapping = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
        'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
        'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        month_number ="0" + str(month_mapping.get(incapacidadAB, 0)) 

        if month_number:
            results = incapacidadesEmp.filter(fecha_inicio__month=month_number)
        else:
            results = models.PERMISO.objects.none() 
        
        return render(request, "incapacidades/incapacidades_filter.html", {"solicitudes": results})

@method_decorator(login_required, name='dispatch')
class Reportes(LoginRequiredMixin, generic.View):

    def get(self, request):
        return render(request, "reporte/reporte_error.html", {})

@method_decorator(login_required, name='dispatch')
class Genera_Reporte(LoginRequiredMixin, generic.CreateView):
    template_name = "reporte/error_form.html"
    model = models.REPORTE
    form_class = forms.ReporteForm
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        form.instance.estado = "Enviado"  
        form.instance.remitente = self.request.user.empleado  
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class Lista_Reportes(LoginRequiredMixin, generic.View):
    template_name = "reporte/reportes_list.html"
    context = {}

    def get(self, request):
        empleado = models.EMPLEADO.objects.get(usuario=request.user)
        
        self.context = {
            "empleado": empleado,
            "reportes": models.REPORTE.objects.filter(remitente=empleado.id),

        }

        return render(request, self.template_name, self.context)

@method_decorator(login_required, name='dispatch')
class Reporte_Estado(LoginRequiredMixin, generic.View):
    template_name = "reporte/reporte_estado.html"
    context = {}

    def get(self, request, pk):
        self.context = {
            "reporte": models.REPORTE.objects.get(id=pk),
        }
        return render(request, self.template_name, self.context)
    
@login_required
def searchReportes(request, *args, **kwargs):
    if request.method == 'GET':
        reporteAB = request.GET.get('busquedaReportes').lower()
        empleado = models.EMPLEADO.objects.get(usuario=request.user)
        reportesEmp = models.REPORTE.objects.filter(remitente=empleado.id)
        
        month_mapping = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
        'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
        'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        month_number ="0" + str(month_mapping.get(reporteAB, 0)) 

        if month_number:
            results = reportesEmp.filter(fecha_inicio__month=month_number)
        else:
            results = models.REPORTE.objects.none() 
        
        return render(request, "reporte/reporte_filter.html", {"reportes": results})