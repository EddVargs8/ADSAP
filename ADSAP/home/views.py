from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from core.models import EMPLEADO
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Home(LoginRequiredMixin, generic.View):
    template_name = "index.html"
    context = {}
    
    def get(self, request):
        rh = request.user.groups.filter(name='Personal RH').exists()
        self.context = {
            'es_rh': rh,    
        }
        return render(request, self.template_name, self.context)
    
@method_decorator(login_required, name='dispatch')
class Cuenta(LoginRequiredMixin, generic.View):
    template_name = "cuenta.html"
    context = {}

    def get(self, request):
        self.context = {

        }
        return render(request, self.template_name, self.context)
    



