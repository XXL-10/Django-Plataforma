from django.shortcuts import render # type: ignore

def home_view(request):
    return render(request, 'Inicio_Sena.html')
