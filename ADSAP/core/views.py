from django.shortcuts import render
from core.models import PREGUNTAS
from core.models import NOTICIAS
from core.models import EMPLEADO
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

@method_decorator(login_required, name='dispatch')
class Home(generic.View):
    template_name = "index.html"
    context = {}

    def get(self, request):
        self.context = {
            "noticia": NOTICIAS.objects.all()
        }
        return render(request, self.template_name, self.context)

@method_decorator(login_required, name='dispatch')
class Preguntas(generic.View):
    template_name = "faq.html"
    context = {}

    def get(self, request):
        self.context = {
            "preguntas": PREGUNTAS.objects.all()
        }

        return render(request, self.template_name, self.context)


def searchPreguntas(request, *args, **kwargs):
    if request.method == 'GET':
        preguntaAB = request.GET.get('busqueda')
        if preguntaAB:
            preguntasAB = PREGUNTAS.objects.filter(pregunta__icontains=preguntaAB)
        else:
            preguntasAB = None
        return render(request, "faq_filter.html", {"preguntasAB": preguntasAB})


@method_decorator(login_required, name='dispatch')
class Noticias(generic.View):
    template_name = "noticia.html"
    context = {}

    def get(self, request):
        self.context = {
            "noticias": NOTICIAS.objects.all()
        }

        return render(request, self.template_name, self.context)

def searchNoticias(request, *args, **kwargs):
    if request.method == 'GET':
        noticiaAB = request.GET.get('busquedaNoticia')
        if noticiaAB:
            noticiasAB = NOTICIAS.objects.filter(Q (titulo__icontains=noticiaAB) | Q(contenido__icontains=noticiaAB) )
        else:
            noticiasAB = None
        return render(request, "noticia_filter.html", {"noticiasAB": noticiasAB})
    
@method_decorator(login_required, name='dispatch')
class DATOS_PERSONALES(generic.View):
    template_name = "datos_personales.html"
    context = {}

    def get(self, request):
        self.context = {
            "empleado": EMPLEADO.objects.get(usuario=request.user)
        }

        return render(request, self.template_name, self.context)