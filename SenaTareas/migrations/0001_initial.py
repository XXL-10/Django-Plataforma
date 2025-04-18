# Generated by Django 5.1.6 on 2025-02-24 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('cc', models.CharField(max_length=20, unique=True)),
                ('numero', models.CharField(max_length=15)),
                ('rol', models.CharField(choices=[('admin', 'Admin'), ('usuario', 'Usuario')], max_length=10)),
                ('contraseña', models.CharField(max_length=255)),
            ],
        ),
    ]
