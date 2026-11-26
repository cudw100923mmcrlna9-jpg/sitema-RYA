from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/estudiante/', views.registro_estudiante, name='registro_estudiante'),
    path('registro/padre/', views.registro_padre, name='registro_padre'),
    path('inicio/', views.dashboard_alumno, name='dashboard_alumno'),
    path('calificaciones/', views.calificaciones_view, name='calificaciones'),
    path('notificaciones/', views.notificaciones_view, name='notificaciones'),
    path('reporte/', views.generar_reporte, name='generar_reporte'),
    path('retardo/', views.generar_retardo, name='generar_retardo'),
    path('justificante/', views.generar_justificante, name='generar_justificante'),
    path('perfil/', views.perfil_alumno, name='perfil_alumno'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('panel-admin/', views.dashboard_admin, name='dashboard_admin'),
]