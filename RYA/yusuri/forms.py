from django import forms
from .models import PerfilEstudiante, DocumentoTramite

class LoginForm(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'nombre completo'})
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control input-pill', 'placeholder': 'correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control input-pill', 'placeholder': 'contraseña'})
    )


class RegistroEstudianteForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'nombre completo'})
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control input-pill', 'placeholder': 'correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control input-pill', 'placeholder': 'contraseña'})
    )
    curp = forms.CharField(
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'curp'})
    )
    numero_control = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'numero de control'})
    )
    grupo = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'grupo'})
    )
    carrera_tecnica = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'carrera tecnica'})
    )
    turno = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'turno'})
    )


class RegistroPadreForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'nombre completo'})
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control input-pill', 'placeholder': 'correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control input-pill', 'placeholder': 'contraseña'})
    )
    curp = forms.CharField(
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'curp'})
    )
    numero_control = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control input-pill', 'placeholder': 'numero de control del estudiante'})
    )

    def clean_numero_control(self):
        nc = self.cleaned_data['numero_control']
        if not PerfilEstudiante.objects.filter(numero_control=nc).exists():
            raise forms.ValidationError("No existe ningún estudiante registrado con ese número de control.")
        return nc


class ReporteForm(forms.ModelForm):
    class Meta:
        model = DocumentoTramite
        fields = ['materia', 'motivo']
        widgets = {
            'materia': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class RetardoForm(forms.ModelForm):
    class Meta:
        model = DocumentoTramite
        fields = ['hora_llegada', 'motivo']
        widgets = {
            'hora_llegada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class JustificanteForm(forms.ModelForm):
    class Meta:
        model = DocumentoTramite
        fields = ['materia', 'motivo']
        widgets = {
            'materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Matemáticas'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones / Motivo de falta'}),
        }