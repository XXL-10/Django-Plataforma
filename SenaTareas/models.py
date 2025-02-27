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
