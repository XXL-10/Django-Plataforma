from django.shortcuts import render # type: ignore

def home_view(request):
    return render(request, 'SenaTareas/Inicio_Sena.html')

def my_view(request):
    return render(request, 'SenaTareas/Inicio_ena.html')

