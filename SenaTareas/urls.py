from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('pagina_instructor/', views.pagina_instructor_view, name='pagina_instructor'),
    path('pagina_aprendiz/', views.pagina_aprendiz_view, name='pagina_aprendiz'),
    path('inicio/', views.inicio_sena, name='inicio_sena'),
    path('logout/', views.logout_view, name='logout'),
    # Otras rutas...
]