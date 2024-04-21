from django.db import models
from users.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class EMPRESA(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=50)
    rfc = models.CharField(max_length=20)
    registro_patronal = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre + " " + self.rfc 

class AREA(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    lider_area = models.ForeignKey('EMPLEADO', on_delete=models.CASCADE, related_name='mi_empleado', null=True, blank=True)

    def __str__(self):
        return self.nombre + " " + self.descripcion 

class EMPLEADO(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    calle = models.CharField(max_length=100)
    numero_casa = models.CharField(max_length=20)
    colonia = models.CharField(max_length=100)
    cp = models.IntegerField()
    municipio = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    curp = models.CharField(max_length=20)
    nss = models.CharField(max_length=20)
    rfc = models.CharField(max_length=20)   
    fecha_nacimiento = models.DateField()
    fecha_ingreso = models.DateField()
    dias_vacaciones = models.IntegerField()
    puesto = models.CharField(max_length=100)
    sexo = models.CharField(max_length=20, choices=(("M", "Masculino"), ("F", "Femenino")), default="Masculino")
    area = models.ForeignKey(AREA, on_delete=models.CASCADE)
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(EMPRESA, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " " + self.puesto

TIPO_PERMISO = (
    ("Personal", "Personal"),
    ("Medico", "Medico"),
    ("Emergencia", "Emergencia"),
    ("Incapacidad", "Incapacidad"),
)

class PERMISO(models.Model): 
    id = models.IntegerField(primary_key=True)
    fecha_solicitud = models.DateField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_PERMISO)
    id_empleado = models.ForeignKey(EMPLEADO, on_delete=models.CASCADE)
    archivo = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.motivo

class VACACIONES(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_solicitud = models.DateField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField(null=True, blank=True)
    id_empleado = models.ForeignKey(EMPLEADO, on_delete=models.CASCADE)

    def __str__(self):
        return self.motivo
    class Meta:
        verbose_name_plural = "Vacaciones"

class NOMINA(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    salario_diario = models.DecimalField(max_digits=10, decimal_places=2)
    horas_trabajadas = models.DecimalField(max_digits=10, decimal_places=2)
    horas_extra = models.DecimalField(max_digits=10, decimal_places=2)
    percepciones = models.DecimalField(max_digits=10, decimal_places=2)
    deducciones = models.DecimalField(max_digits=10, decimal_places=2)
    id_empleado = models.ForeignKey(EMPLEADO, on_delete=models.CASCADE)


class NOTICIAS(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateField()
    id_area = models.ForeignKey(AREA, on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(null=True, blank=True); 

    def __str__(self):
        return self.titulo + " " + self.contenido 
    class Meta:
        db_table = "core_noticia"
        verbose_name_plural = "Noticias"

class PREGUNTAS(models.Model):
    id = models.IntegerField(primary_key=True)
    pregunta = models.TextField()
    respuesta = models.TextField()
    imagen = models.ImageField(null=True, blank=True); 

    def __str__(self):
        return self.pregunta + " " + self.respuesta
    class Meta:
        db_table = "core_pregunta"
        verbose_name_plural = "Preguntas"

ESTADO = (
    ("Aceptado", "Aceptado"),
    ("Rechazado", "Rechazado"),
    ("En revision", "En revision"),
    ("Cancelado", "Cancelado"),
)

class ESTADO_SOLICITUD(models.Model):
    id = models.IntegerField(primary_key=True)
    estado = models.CharField(max_length=20, choices=ESTADO)
    comentarios_admin = models.TextField(null=True, blank=True)
    #id de solicitud 
    id_vacaciones = models.ForeignKey(VACACIONES, on_delete=models.CASCADE, null=True, blank=True)
    id_permiso = models.ForeignKey(PERMISO, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.estado + " " + self.comentarios_admin + " " 
    class Meta:
        verbose_name_plural = "Estado de solicitudes"

REPORTE = (
    ("Enviado", "Enviado"),
    ("En revision", "En revision"),
    ("Corregido", "Corregido"),
)
SECCION = (
    ("Login", "Inicio de Sesion"),
    ("Permisos", "Permisos"),
    ("Vacaciones", "Vacaciones"),
    ("Nomina", "Nomina"),
    ("Noticias", "Noticias"),
    ("Preguntas", "Preguntas"), 
    ("Datos personales", "Datos personales"),
    ("Otro", "Otro")
)

#REPORTE
class REPORTE(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField()
    remitente = models.ForeignKey(EMPLEADO, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=REPORTE)
    seccion = models.CharField(max_length=20, choices=SECCION, null=True, blank=True)
    imagen = models.ImageField(null=True, blank=True); 

    def __str__(self):
        return self.descripcion