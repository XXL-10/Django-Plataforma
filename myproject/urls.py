from django.contrib import admin
from django.urls import path, include
from SenaTareas.views import home_view, login_view, pagina_instructor_view, pagina_aprendiz_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SenaTareas.urls')),
]
