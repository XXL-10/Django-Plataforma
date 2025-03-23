from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import json
import random
import string
from .models import User, Curso
from datetime import datetime
from django.contrib import messages

# Función para generar una contraseña aleatoria
def generar_contraseña():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=8))  # Genera una contraseña de 8 caracteres

# Vista de la página de inicio
def home_view(request):
    return render(request, 'SenaTareas/Inicio_Sena.html')

# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        cc = request.POST.get('cc')
        password = request.POST.get('password')

        if not cc or not password:
            messages.error(request, 'Por favor, ingresa tu cédula y contraseña.')
            return render(request, 'SenaTareas/Inicio_Sena.html')

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

# Vista de la página del instructor
@login_required
def pagina_instructor_view(request):
    if request.user.rol != 'instructor':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')
    
    # Obtener todos los cursos de la base de datos
    cursos = Curso.objects.all()
    return render(request, 'SenaTareas/pagina_instructor.html', {'cursos': cursos})

# Vista de la página del aprendiz
@login_required
def pagina_aprendiz_view(request):
    if request.user.rol != 'aprendiz':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')
    return render(request, 'SenaTareas/pagina_aprendiz.html')

# Vista de inicio de sesión (alternativa)
def inicio_sena(request):
    if request.user.is_authenticated:
        if request.user.rol == 'instructor':
            return redirect('pagina_instructor')
        elif request.user.rol == 'aprendiz':
            return redirect('pagina_aprendiz')
    
    if request.method == 'POST':
        cc = request.POST.get('cc')
        password = request.POST.get('password')

        if not cc or not password:
            messages.error(request, 'Por favor, ingresa tu cédula y contraseña.')
            return render(request, 'SenaTareas/Inicio_Sena.html')

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

# Vista para cerrar sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista para recuperar contraseña
@csrf_exempt
def recuperar_contraseña(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            cc = data.get('cc')
            telefono = data.get('telefono')

            if not all([nombre, apellido, cc, telefono]):
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios.'})

            try:
                user = User.objects.get(nombre=nombre, apellido=apellido, cc=cc, telefono=telefono)
                
                # Generar una nueva contraseña
                nueva_contraseña = generar_contraseña()
                user.set_password(nueva_contraseña)  # Guardar la nueva contraseña en formato hash
                user.save()

                return JsonResponse({'success': True, 'password': nueva_contraseña})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No se encontró un usuario con estos datos.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error en el formato de los datos.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# Vista para crear un curso
@csrf_exempt
def crear_curso(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            ficha = request.POST.get('ficha')
            nombre = request.POST.get('nombre')
            tipo = request.POST.get('tipo')
            sede = request.POST.get('sede', None)  # Sede es opcional
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_finalizacion = request.POST.get('fecha_finalizacion')

            # Validar que los campos obligatorios estén presentes
            if not all([ficha, nombre, tipo, fecha_inicio, fecha_finalizacion]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('pagina_instructor')

            # Convertir las fechas a objetos date
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_finalizacion = datetime.strptime(fecha_finalizacion, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Formato de fecha inválido. Use YYYY-MM-DD.')
                return redirect('pagina_instructor')

            # Validar que la fecha de inicio sea anterior a la fecha de finalización
            if fecha_inicio >= fecha_finalizacion:
                messages.error(request, 'La fecha de inicio debe ser anterior a la fecha de finalización.')
                return redirect('pagina_instructor')

            # Validar que la ficha no esté duplicada
            if Curso.objects.filter(ficha=ficha).exists():
                messages.error(request, 'El número de ficha ya está en uso.')
                return redirect('pagina_instructor')

            # Crear el curso
            curso = Curso.objects.create(
                ficha=ficha,
                nombre=nombre,
                tipo=tipo,
                sede=sede if tipo == 'presencial' else None,  # Solo guardar sede si es presencial
                fecha_inicio=fecha_inicio,
                fecha_finalizacion=fecha_finalizacion
            )

            messages.success(request, 'Curso creado exitosamente.')
            return redirect('pagina_instructor')  # Redirigir a la página del instructor o donde corresponda

        except IntegrityError:
            messages.error(request, 'Error de integridad en la base de datos. Verifica los datos.')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error al crear el curso: {str(e)}')

        return redirect('pagina_instructor')

    return redirect('pagina_instructor')
# Vista para editar un curso
@csrf_exempt
def editar_curso(request, curso_id):
    if request.method == 'POST':
        try:
            curso = get_object_or_404(Curso, id=curso_id)
            curso.nombre = request.POST.get('nombre')
            curso.tipo = request.POST.get('tipo')
            curso.sede = request.POST.get('sede', None)
            curso.fecha_inicio = request.POST.get('fecha_inicio')
            curso.fecha_finalizacion = request.POST.get('fecha_finalizacion')
            curso.save()
            return JsonResponse({'success': True, 'message': 'Curso actualizado exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al actualizar el curso: {str(e)}'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# Vista para eliminar un curso
@csrf_exempt
def eliminar_curso(request, curso_id):
    if request.method == 'POST':
        try:
            curso = get_object_or_404(Curso, id=curso_id)
            curso.delete()
            return JsonResponse({'success': True, 'message': 'Curso eliminado exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al eliminar el curso: {str(e)}'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def curso_detalle(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, 'SenaTareas/curso_detalle.html', {'curso': curso})
