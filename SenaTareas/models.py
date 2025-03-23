from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, cc, password=None, **extra_fields):
        if not cc:
            raise ValueError('The Cédula de Ciudadanía field must be set')
        user = self.model(cc=cc, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cc, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cc, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    cc = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=20, choices=[('instructor', 'Instructor'), ('aprendiz', 'Aprendiz')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'cc'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'telefono', 'rol']

    def __str__(self):
        return self.cc
class Curso(models.Model):
    
    
    # Opciones para el campo 'tipo'
    TIPO_CHOICES = [
        ('presencial', 'Presencial'),
        ('digital', 'Digital'),
    ]

    ficha = models.PositiveIntegerField(unique=True, help_text="Número de ficha (debe ser mayor o igual a 1000)")
    nombre = models.CharField(max_length=200, help_text="Nombre del curso")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, help_text="Tipo de curso (Presencial o Digital)")
    sede = models.CharField(max_length=100, blank=True, null=True, help_text="Sede del curso (solo si es presencial)")
    fecha_inicio = models.DateField(help_text="Fecha de inicio del curso")
    fecha_finalizacion = models.DateField(help_text="Fecha de finalización del curso")

    def __str__(self):
        return f"{self.ficha} - {self.nombre}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"