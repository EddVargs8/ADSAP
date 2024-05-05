from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import HttpResponse, HttpResponseForbidden
from core import models 
from users import models as users_models
from RH import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist

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
        self.context = {
            
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
            return render(request, "RH/Empleados/empleado_filter.html", {"empleado": empleado, "usuario": usuario})
        else:
            return HttpResponse('Empleado no encontrado', status=404)

@method_decorator(login_required, name='dispatch')
class Elimina_Empleados(LoginRequiredMixin, generic.DeleteView):
    model = users_models.CustomUser
    template_name = "RH/Empleados/empleado_eliminado_confirmacion.html"
    success_url = reverse_lazy("RH:empleados")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Personal RH').exists():
            return HttpResponseForbidden("No estás autorizado para ver esta página.")
        return super().dispatch(request, *args, **kwargs)

