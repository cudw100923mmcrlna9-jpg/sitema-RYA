from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, PerfilEstudiante, PerfilPadre, Asistencia
from .forms import (
    LoginForm,
    RegistroEstudianteForm,
    RegistroPadreForm,
    ReporteForm,
)

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        correo = form.cleaned_data['correo']
        password = form.cleaned_data['password']
        user = authenticate(request, username=correo, password=password)
        if user is not None:
            login(request, user)
            if user.rol == 'admin':
                return redirect('dashboard_admin')
            return redirect('dashboard_alumno')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def registro_estudiante(request):
    form = RegistroEstudianteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        user = Usuario.objects.create_user(
            username=data['correo'],
            email=data['correo'],
            password=data['password'],
            nombre_completo=data['nombre'],
            rol='estudiante'
        )
        PerfilEstudiante.objects.create(
            usuario=user,
            curp=data['curp'],
            numero_control=data['numero_control'],
            grupo=data['grupo'],
            carrera_tecnica=data['carrera_tecnica'],
            turno=data['turno']
        )
        messages.success(request, 'Perfil de estudiante creado correctamente.')
        return redirect('login')
    return render(request, 'auth/registro_estudiante.html', {'form': form})


def registro_padre(request):
    form = RegistroPadreForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        estudiante = PerfilEstudiante.objects.get(numero_control=data['numero_control'])
        user = Usuario.objects.create_user(
            username=data['correo'],
            email=data['correo'],
            password=data['password'],
            nombre_completo=data['nombre'],
            rol='padre'
        )
        PerfilPadre.objects.create(
            usuario=user,
            curp=data['curp'],
            estudiante=estudiante
        )
        messages.success(request, 'Perfil de padre de familia registrado.')
        return redirect('login')
    return render(request, 'auth/registro_padre.html', {'form': form})


@login_required
def dashboard_alumno(request):
    perfil = getattr(request.user, 'perfil_estudiante', None)
    asistencias = Asistencia.objects.filter(estudiante=perfil) if perfil else []
    return render(request, 'alumno/dashboard.html', {
        'perfil': perfil,
        'asistencias': asistencias,
    })


@login_required
def generar_reporte(request):
    form = ReporteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        reporte = form.save(commit=False)
        reporte.estudiante = request.user.perfil_estudiante
        reporte.tipo = 'reporte'
        reporte.save()
        messages.success(request, 'Reporte generado correctamente.')
        return redirect('dashboard_alumno')
    return render(request, 'alumno/generar_reporte.html', {'form': form})



@login_required
def perfil_alumno(request):
    perfil = getattr(request.user, 'perfil_estudiante', None)
    return render(request, 'alumno/perfil.html', {'perfil': perfil})



@login_required
def dashboard_admin(request):
    total_alumnos = PerfilEstudiante.objects.count()
    presentes = Asistencia.objects.filter(estado='asistencia').count()
    retardos = Asistencia.objects.filter(estado='retardo').count()
    faltas = Asistencia.objects.filter(estado='falta').count()
    return render(request, 'admin_panel/dashboard_admin.html', {
        'total_alumnos': total_alumnos,
        'presentes': presentes,
        'retardos': retardos,
        'faltas': faltas,
    })