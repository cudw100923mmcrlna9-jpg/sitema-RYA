from django.db import models

# Create your models here.
class Alumno(models.Model):
    no_control = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.CharField(max_length=50)
    grupo = models.PositiveIntegerField()
    nacimiento = models.DateTimeField(auto_now_add=True)
    curp = models.CharField(max_length=50)
    correo = models.EmailField()
    turno = models.CharField(max_length=50)
    carrera = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class Profesores(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.CharField(max_length=50)
    curp = models.CharField(max_length=50)
    correo = models.EmailField()
    carrera = models.CharField(max_length=50)
    grupo_cargo = models.PositiveIntegerField()
    pase_lista = models.CharField(max_length=50)
    no_control = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class Administrador(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.CharField(max_length=50)
    curp = models.CharField(max_length=50)
    correo = models.EmailField()
    
    
    def __str__(self):
        return self.nombre
    
class Tutor(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.CharField(max_length=50)
    curp = models.CharField(max_length=50)
    correo = models.EmailField()
    
    
    def __str__(self):
        return self.nombre
    
class generar_reporte(models.Model):
    clave_reporte = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    grupo = models.PositiveIntegerField()
    turno = models.CharField(max_length=50)
    carrera = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=50)
    compromiso = models.TextField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    firma = models.TextField(max_length=50)    
    
    def __str__(self):
        return self.nombre