from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, PerfilEstudiante, PerfilPadre, Calificacion, Asistencia, DocumentoTramite, Notificacion
from .forms import (
    LoginForm,
    RegistroEstudianteForm,
    RegistroPadreForm,
    ReporteForm,
    RetardoForm,
    JustificanteForm,
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
def calificaciones_view(request):
    semestre = int(request.GET.get('semestre', 3))
    perfil = getattr(request.user, 'perfil_estudiante', None)
    califs = Calificacion.objects.filter(estudiante=perfil, semestre=semestre) if perfil else []
    return render(request, 'alumno/calificaciones.html', {
        'califs': califs,
        'semestre_actual': semestre
    })


@login_required
def notificaciones_view(request):
    notifs = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'alumno/notificaciones.html', {'notificaciones': notifs})


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
def generar_retardo(request):
    form = RetardoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        retardo = form.save(commit=False)
        retardo.estudiante = request.user.perfil_estudiante
        retardo.tipo = 'retardo'
        retardo.save()
        messages.success(request, 'Retardo registrado correctamente.')
        return redirect('dashboard_alumno')
    return render(request, 'alumno/generar_retardo.html', {'form': form})


@login_required
def generar_justificante(request):
    form = JustificanteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        justificante = form.save(commit=False)
        justificante.estudiante = request.user.perfil_estudiante
        justificante.tipo = 'justificante'
        justificante.save()
        messages.success(request, 'Solicitud de justificante enviada.')
        return redirect('dashboard_alumno')
    return render(request, 'alumno/generar_justificante.html', {'form': form})


@login_required
def perfil_alumno(request):
    perfil = getattr(request.user, 'perfil_estudiante', None)
    return render(request, 'alumno/perfil.html', {'perfil': perfil})


@login_required
def calendario_view(request):
    return render(request, 'alumno/calendario.html')


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