from django.urls import path
from users import views
from django.contrib.auth import views as auth_views


app_name = "users"



urlpatterns = [
    path('', views.custom_login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/cambio_contrasena.html"), name="reset_password"),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/cambio_contrasena_enviado.html"), name="password_reset_done"),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/cambio_contrasena_form.html"), name="password_reset_confirm"),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/cambio_contrasena_hecho.html"), name="password_reset_complete"),
]