from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    return redirect('home')