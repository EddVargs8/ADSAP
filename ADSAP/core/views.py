from django.shortcuts import render
from core.models import PREGUNTAS
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class Preguntas(generic.View):
    template_name = "faq.html"
    context = {}

    def get(self, request):
        self.context = {
            "preguntas": PREGUNTAS.objects.all()
        }

        return render(request, self.template_name, self.context)