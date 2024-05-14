from django.urls import path
from RH import views

app_name = "RH"

urlpatterns = [
    path('empleados/', views.Empleados.as_view(), name="empleados"),
    path('empleados/crea', views.Crea_Empleados.as_view(), name="crea_empleados"),
    path('empleados/crea/<int:user_id>/', views.Crea_Empleados2.as_view(), name="crea_empleados2"),
    path('empleados/editar/empleado/', views.Edita_Empleados_Busqueda.as_view(), name="editar_empleado_busqueda"),
    path('empleados/editar/empleado/filtro/', views.Edita_Empleados_List.as_view(), name='editar_empleados_list'),
    path('empleados/editar/empleado/<int:pk>/', views.Edita_Empleados.as_view(), name='editar_empleado'),
    path('empleados/editar/empleado/eliminar/<int:pk>/', views.Elimina_Empleados.as_view(), name='eliminar_empleado'),
    path('administra_vacaciones/', views.Vacaciones_Busqueda.as_view(), name="vacaciones_busqueda"),
    path('administra_vacaciones/estado/<int:pk>/', views.Edita_Vacaciones.as_view(), name="vacaciones_estado"),
    path('administra_vacaciones/filtro/', views.searchVacaciones, name="vacaciones_filtro"),
    path('administra_permisos/', views.Permisos_Busqueda.as_view(), name="permisos_busqueda"),
    path('administra_permisos/estado/<int:pk>/', views.Edita_Permisos.as_view(), name="permisos_estado"),
    path('administra_permisos/filtro/', views.searchPermisos, name="permisos_filtro"),
    path('administra_noticas/', views.Noticias.as_view(), name="noticias"),
    path('administra_noticas/crea/', views.Crea_Noticias.as_view(), name="crea_noticias"),
    path('administra_noticas/lista/', views.ListarNoticias.as_view(), name="lista_noticias"),
    path('administra_noticas/detalle/<int:pk>/', views.DetallesNoticia.as_view(), name="detalles_noticias"),
    path('administra_noticas/editar/<int:pk>/', views.Edita_Noticias.as_view(), name="editar_noticias"),
    path('administra_noticas/eliminar/<int:pk>/', views.Elimina_Noticia.as_view(), name="eliminar_noticias"),
    path('administra_noticas/lista/filtro/', views.searchNoticias, name="noticias_filtro"),
    path('administra_faqs/', views.Preguntas.as_view(), name="faqs"),
    path('administra_faqs/crea/', views.Crea_Preguntas.as_view(), name="crea_faqs"),
    path('administra_faqs/lista/', views.ListarPreguntas.as_view(), name="lista_faqs"),
    path('administra_faqs/detalle/<int:pk>/', views.DetallesPregunta.as_view(), name="detalles_faqs"),
    path('administra_faqs/editar/<int:pk>/', views.Edita_Preguntas.as_view(), name="editar_faqs"),
    path('administra_faqs/eliminar/<int:pk>/', views.Elimina_Pregunta.as_view(), name="eliminar_faqs"),
    path('administra_faqs/lista/filtro/', views.searchPreguntas, name="faqs_filtro"),
    


]