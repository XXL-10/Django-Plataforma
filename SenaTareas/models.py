from django.db import models # type: ignore

# Create your models here.
class Tarea(models.Model):
    nombre = models.CharField(max_length=250)