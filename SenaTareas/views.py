from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import random
import string
from .models import User

def generar_contraseña():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=8))  # Genera una contraseña de 8 caracteres

def home_view(request):
    return render(request, 'SenaTareas/Inicio_Sena.html')

def login_view(request):
    if request.method == 'POST':
        cc = request.POST['cc']
        password = request.POST['password']
        user = authenticate(request, username=cc, password=password)
        if user is not None:
            login(request, user)
            if user.rol == 'instructor':
                return redirect('pagina_instructor')
            elif user.rol == 'aprendiz':
                return redirect('pagina_aprendiz')
        else:
            messages.error(request, 'Cédula de Ciudadanía o contraseña incorrecta.')
    return render(request, 'SenaTareas/Inicio_Sena.html')

@login_required
def pagina_instructor_view(request):
    if request.user.rol != 'instructor':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')
    return render(request, 'SenaTareas/pagina_instructor.html')

@login_required
def pagina_aprendiz_view(request):
    if request.user.rol != 'aprendiz':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')
    return render(request, 'SenaTareas/pagina_aprendiz.html')

def inicio_sena(request):
    if request.user.is_authenticated:
        if request.user.rol == 'instructor':
            return redirect('pagina_instructor')
        elif request.user.rol == 'aprendiz':
            return redirect('pagina_aprendiz')
    
    if request.method == 'POST':
        cc = request.POST['cc']
        password = request.POST['password']
        user = authenticate(request, username=cc, password=password)
        if user is not None:
            login(request, user)
            if user.rol == 'instructor':
                return redirect('pagina_instructor')
            elif user.rol == 'aprendiz':
                return redirect('pagina_aprendiz')
        else:
            messages.error(request, 'Cédula de Ciudadanía o contraseña incorrecta.')
    return render(request, 'SenaTareas/Inicio_Sena.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def recuperar_contraseña(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        cc = data.get('cc')
        telefono = data.get('telefono')

        try:
            user = User.objects.get(nombre=nombre, apellido=apellido, cc=cc, telefono=telefono)
            
            # Generar una nueva contraseña
            nueva_contraseña = generar_contraseña()
            user.set_password(nueva_contraseña)  # Guardar la nueva contraseña en formato hash
            user.save()

            return JsonResponse({'success': True, 'password': nueva_contraseña})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No se encontró un usuario con estos datos'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})