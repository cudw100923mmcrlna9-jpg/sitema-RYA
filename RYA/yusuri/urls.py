from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/estudiante/', views.registro_estudiante, name='registro_estudiante'),
    path('registro/padre/', views.registro_padre, name='registro_padre'),
    path('inicio/', views.dashboard_alumno, name='dashboard_alumno'),
    path('reporte/', views.generar_reporte, name='generar_reporte'),
    path('perfil/', views.perfil_alumno, name='perfil_alumno'),
    path('panel-admin/', views.dashboard_admin, name='dashboard_admin'),
]