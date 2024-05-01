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

@method_decorator(login_required, name='dispatch')
class Home(LoginRequiredMixin, generic.View):
    template_name = "index.html"
    context = {}

    def get(self, request):
        self.context = {
            "noticia": models.NOTICIAS.objects.all()
        }
        return render(request, self.template_name, self.context)

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
    template_name = "vacaciones.html"
    context = {}

    def get(self, request):
        self.context = {
            "empleado": models.EMPLEADO.objects.get(usuario=request.user),
            "solicitudes": models.VACACIONES.objects.all(),
            "dias_solicitados": models.VACACIONES.dias_solicitados
        }

        return render(request, self.template_name, self.context)

@method_decorator(login_required, name='dispatch')
class Vacaciones_Confirmacion(LoginRequiredMixin, generic.View):
    template_name = "vacaciones_confirmacion.html"
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

    return render(request, 'form_vacaciones.html', {'form': form})
    
@method_decorator(login_required, name='dispatch')
class Vacaciones_Estado(LoginRequiredMixin, generic.View):
    template_name = "vacaciones_estado.html"
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
    template_name = "vacaciones_eliminacion.html"
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

        month_mapping = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
        'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
        'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        month_number ="0" + str(month_mapping.get(vacacionesAB, 0)) 

        if month_number:
            results = models.VACACIONES.objects.filter(fecha_inicio__month=month_number)
        else:
            results = models.VACACIONES.objects.none() 
        return render(request, "vacaciones_filter.html", {"vacaciones": results})
