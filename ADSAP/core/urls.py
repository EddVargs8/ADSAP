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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)