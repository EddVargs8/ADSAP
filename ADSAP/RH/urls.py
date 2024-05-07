from django.urls import path
from RH import views

app_name = "RH"

urlpatterns = [
    path('Empleados/', views.Empleados.as_view(), name="empleados"),
    path('Empleados/Crea', views.Crea_Empleados.as_view(), name="crea_empleados"),
    path('Empleados/Crea/<int:user_id>/', views.Crea_Empleados2.as_view(), name="crea_empleados2"),
    path('Empleados/Editar/Empleado/', views.Edita_Empleados_Busqueda.as_view(), name="editar_empleado_busqueda"),
    path('Empleados/Editar/Empleado/filtro/', views.Edita_Empleados_List.as_view(), name='editar_empleados_list'),
    path('Empleados/Editar/Empleado/<int:pk>/', views.Edita_Empleados.as_view(), name='editar_empleado'),
    path('Empleados/Editar/Empleado/Eliminar/<int:pk>/', views.Elimina_Empleados.as_view(), name='eliminar_empleado'),
    path('Administra_Vacaciones/', views.Vacaciones.as_view(), name="vacaciones"),
    path('Administra_Vacaciones/Busqueda', views.Vacaciones_Busqueda.as_view(), name="vacaciones_busqueda"),



]