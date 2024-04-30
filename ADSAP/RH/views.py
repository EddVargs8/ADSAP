from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class Home_RH(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "RH/index_rh.html"
    context = {}

    def test_func(self):
        is_admin = self.request.user.groups.filter(name='Personal RH').exists()
        print("RH:", is_admin)  # Solo para propósitos de depuración
        return is_admin

    def get(self, request, *args, **kwargs):
        self.context = {
            
        }

        return render(request, self.template_name, self.context)