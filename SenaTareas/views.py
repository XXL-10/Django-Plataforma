from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User

def home_view(request):
    return render(request, 'SenaTareas/Inicio_Sena.html')

def login_view(request):
    if request.method == 'POST':
        cc = request.POST['cc']
        password = request.POST['password']
        user = authenticate(request, username=cc, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Cédula de Ciudadanía o contraseña incorrecta.')
    return render(request, 'SenaTareas/login.html')

def pagina_instructor_view(request):
    return render(request, 'SenaTareas/pagina_instructor.html')

def pagina_aprendiz_view(request):
    return render(request, 'SenaTareas/pagina_aprendiz.html')

def inicio_sena(request):
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

