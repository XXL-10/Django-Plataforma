from django.urls import path
from . import views
from .views import curso_detalle

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('pagina_instructor/', views.pagina_instructor_view, name='pagina_instructor'),
    path('pagina_aprendiz/', views.pagina_aprendiz_view, name='pagina_aprendiz'),
    path('inicio/', views.inicio_sena, name='inicio_sena'),
    path('logout/', views.logout_view, name='logout'),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),
    path('crear_curso/', views.crear_curso, name='crear_curso'),
    path('editar_curso/<int:curso_id>/', views.editar_curso, name='editar_curso'),  
    path('eliminar_curso/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'),
    path('curso/<int:curso_id>/', curso_detalle, name='curso_detalle'), 
]