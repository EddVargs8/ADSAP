from django.urls import path
from core import views

app_name = "core"


urlpatterns = [
    path('faq/', views.Preguntas.as_view(), name="faq")
]
