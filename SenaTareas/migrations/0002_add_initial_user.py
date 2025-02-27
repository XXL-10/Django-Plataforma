from django.db import migrations
from django.contrib.auth.hashers import make_password

def add_initial_user(apps, schema_editor):
    Usuario = apps.get_model('SenaTareas', 'Usuario')
    usuario = Usuario(
        nombre='Nombre',
        apellido='Apellido',
        cc='1006408587',
        numero='1234567890',
        rol='instructor',
        contraseña=make_password('password123')
    )
    usuario.save()

class Migration(migrations.Migration):

    dependencies = [
        ('SenaTareas', '0001_initial'),  # Asegúrate de que esta sea la última migración existente
    ]

    operations = [
        migrations.RunPython(add_initial_user),
    ]