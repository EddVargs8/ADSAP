from django.urls import path
from home import views

app_name = "home"

urlpatterns = [
    path('home/', views.Home.as_view(), name="home"),
    path('cuenta/', views.Cuenta.as_view(), name="cuenta"),

]