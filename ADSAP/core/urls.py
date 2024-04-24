from django.urls import path, re_path
from core import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path('faq/', views.Preguntas.as_view(), name="faq"),
    path('faq/filtro', views.searchPreguntas, name="faq_filter"),
    path('noticias/', views.Noticias.as_view(), name="noticias"),
    path('noticias/filtro', views.searchNoticias, name="noticias_filter"),
    path('datos_personales', views.Datos_Personales.as_view(), name="datos_personales"),
    path('vacaciones', views.Vacaciones.as_view(), name="vacaciones"),
    path('vacaciones/solicitud', views.Vacaciones_Form, name="vacaciones_solicitud"),
    path('vacaciones/solicitud/confirmacion', views.Vacaciones_Confirmacion.as_view(), name="vacaciones_confirmacion"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)