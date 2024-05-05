from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from core.models import EMPLEADO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@method_decorator(login_required, name='dispatch')
class Home(LoginRequiredMixin, generic.View):
    def get(self, request):
        context = {}

        try:
            if request.user.groups.filter(name='Empleados').exists():
                template_name = "index.html"
            elif request.user.groups.filter(name='Personal RH').exists():
                template_name = "RH/index_rh.html"
            else:  # Lógica de Administrador
                template_name = "RH/index_rh.html" 
            return render(request, template_name, context)
        except ObjectDoesNotExist:
            pass

        
    
@method_decorator(login_required, name='dispatch')
class Cuenta(LoginRequiredMixin, generic.View):
    template_name = "cuenta.html"
    context = {}

    def get(self, request):
        self.context = {

        }
        return render(request, self.template_name, self.context)
    



