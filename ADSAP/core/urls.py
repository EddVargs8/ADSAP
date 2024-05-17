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
    path('vacaciones/filtro', views.searchVacaciones, name="vacaciones_filter"),
    path('vacaciones/solicitud', views.Vacaciones_Form, name="vacaciones_solicitud"),
    path('vacaciones/solicitud/confirmacion', views.Vacaciones_Confirmacion.as_view(), name="vacaciones_confirmacion"),
    path('vacaciones/solicitud/estado/<int:pk>/', views.Vacaciones_Estado.as_view(), name="vacaciones_estado"),
    path('vacaciones/solicitud/eliminar/<int:pk>/', views.Vacaciones_Eliminacion.as_view(), name="vacaciones_eliminar_confirmacion"),
    path('permisos', views.Permisos.as_view(), name="permisos"),
    path('permisos/solicitud', views.Permisos_Form, name="permisos_solicitud"),
    path('permisos/solicitud/confirmacion', views.Permisos_Confirmacion.as_view(), name="permisos_confirmacion"),
    path('permisos/solicitud/estado/<int:pk>/', views.Permisos_Estado.as_view(), name="permisos_estado"),
    path('permisos/solicitud/eliminar/<int:pk>/', views.Permisos_Eliminacion.as_view(), name="permisos_eliminar_confirmacion"),
    path('permisos/filtro', views.searchPermisos, name="permisos_filter"),
    path('incapacidades', views.Incapacidades.as_view(), name="incapacidades"),
    path('incapacidades/detalle/<int:pk>/', views.Incapacidades_Detalles.as_view(), name="incapacidad_detalle"),
    path('incapacidades/solicitud', views.Incapacidades_Form, name="incapacidades_solicitud"),
    path('incapacidades/filtro', views.searchIncapacidades, name="incapacidades_filter"),
    path('reporte_error', views.Reportes.as_view(), name="reporte_error"),
    path('reporte_error/genera', views.Genera_Reporte.as_view(), name="genera_reporte"),
    path('reporte_error/lista/', views.Lista_Reportes.as_view(), name="reporte_lista"),
    path('reporte_error/detalle/<int:pk>/', views.Reporte_Estado.as_view(), name="reporte_detalle"),
    path('reporte_error/lista/filtro/', views.searchReportes, name="reporte_filtro"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)