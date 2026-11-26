from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('padre', 'Padre de Familia'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    nombre_completo = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre_completo} ({self.get_rol_display()})"


class PerfilEstudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_estudiante')
    curp = models.CharField(max_length=18, unique=True)
    numero_control = models.CharField(max_length=20, unique=True)
    grupo = models.CharField(max_length=10)
    semestre = models.IntegerField(default=3)
    carrera_tecnica = models.CharField(max_length=100)
    turno = models.CharField(max_length=20)
    plantel = models.CharField(max_length=100, default='CECyTEM')
    localidad = models.CharField(max_length=100, blank=True)
    promedio_general = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    estado_nacimiento = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=15, blank=True)
    enfermedades = models.TextField(blank=True, default='Ninguna')
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.numero_control}"


class PerfilPadre(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_padre')
    curp = models.CharField(max_length=18)
    estudiante = models.ForeignKey(PerfilEstudiante, on_delete=models.CASCADE, related_name='padres')

    def __str__(self):
        return f"Padre: {self.usuario.nombre_completo} -> Alumno: {self.estudiante.numero_control}"


class Calificacion(models.Model):
    estudiante = models.ForeignKey(PerfilEstudiante, on_delete=models.CASCADE, related_name='calificaciones')
    semestre = models.IntegerField(default=3)
    materia = models.CharField(max_length=100)
    parcial_1 = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    parcial_2 = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    parcial_3 = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)

    @property
    def total(self):
        return round((self.parcial_1 + self.parcial_2 + self.parcial_3) / 3, 1)

    def __str__(self):
        return f"{self.materia} - {self.estudiante.numero_control}"


class Asistencia(models.Model):
    ESTADOS = (
        ('asistencia', 'Asistencia'),
        ('falta', 'Falta'),
        ('retardo', 'Retardo'),
    )
    estudiante = models.ForeignKey(PerfilEstudiante, on_delete=models.CASCADE, related_name='asistencias')
    materia = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADOS)

    def __str__(self):
        return f"{self.estudiante.numero_control} | {self.materia} | {self.estado}"


class DocumentoTramite(models.Model):
    TIPOS = (
        ('reporte', 'Reporte'),
        ('retardo', 'Retardo'),
        ('justificante', 'Justificante'),
    )
    estudiante = models.ForeignKey(PerfilEstudiante, on_delete=models.CASCADE, related_name='tramites')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    materia = models.CharField(max_length=100, blank=True)
    fecha = models.DateField(auto_now_add=True)
    hora_llegada = models.TimeField(null=True, blank=True)
    motivo = models.TextField()
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.estudiante.usuario.nombre_completo}"


class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre_completo}: {self.mensaje[:30]}"