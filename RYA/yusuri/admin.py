from django.contrib import admin
from django.contrib import admin
from .models import Usuario, PerfilEstudiante, PerfilPadre, Calificacion, Asistencia, DocumentoTramite, Notificacion
# Register your models here.


admin.site.register(Usuario)
admin.site.register(PerfilEstudiante)
admin.site.register(PerfilPadre)
admin.site.register(DocumentoTramite)
