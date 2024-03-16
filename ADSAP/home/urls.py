from django.urls import path
from home import views
from django.contrib.auth import views as auth_views

app_name = "home"


urlpatterns = [
    path('', views.Login.as_view(), name="login"),
    path('home/', views.Home.as_view(), name="home"),
    path('cuenta/', views.Cuenta.as_view(), name="cuenta"),
    path('faq/', views.Faq.as_view(), name="faq"),
    path( "logout/", auth_views.LogoutView.as_view() , name="logout")
]