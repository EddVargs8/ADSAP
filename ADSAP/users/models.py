from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    #numero_empleado va en el modelo de empleado
    numero_empleado = models.CharField(max_length=10, unique=True)

    REQUIRED_FIELDS = ['email', 'numero_empleado'] 