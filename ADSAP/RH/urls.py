from django.urls import path
from RH import views

app_name = "RH"

urlpatterns = [
    path('homeRH/', views.Home_RH.as_view(), name="home_RH"),
]