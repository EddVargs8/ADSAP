from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from core.models import EMPLEADO

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Home(generic.View):
    template_name = "index.html"
    context = {}

    def get(self, request):
        self.context = {
            "empleado" : EMPLEADO.objects.get(usuario=request.user)
        }
        return render(request, self.template_name, self.context)
    
@method_decorator(login_required, name='dispatch')
class Cuenta(generic.View):
    template_name = "cuenta.html"
    context = {}

    def get(self, request):
        self.context = {

        }
        return render(request, self.template_name, self.context)
    



