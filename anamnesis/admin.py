# formulario/admin.py

import re
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Importamos ModelForm y UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser  

# --- 1. Formulario de CREACIÓN Personalizado ---
class CustomUserCreationForm(ModelForm):
    
    # --- Definimos TODOS los campos para añadir el help_text ---
    
    # Username (sin validador estricto)
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        help_text=_(
            "Requerido. 150 caracteres o menos. "
            "Letras, números y caracteres especiales permitidos."
        ),
    )
    
    # Email como texto simple (requerido)
    email = forms.CharField(
        label='Correo (Requerido)', 
        max_length=254
    )
    
    # Campos con validación y help_text
    first_name = forms.CharField(label='Nombre', max_length=150)
    last_name = forms.CharField(label='Apellido Paterno', max_length=150)
    
    rut = forms.CharField(
        label='RUT', 
        max_length=12, 
        help_text='Formato: 12.345.678-9' # <--- ¡AQUÍ ESTÁ!
    )
    telefono = forms.CharField(
        label='Teléfono', 
        max_length=15, 
        help_text='Formato: 9 1234 5678' # <--- ¡Y AQUÍ!
    )
    
    # Password Único
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        # Campos que el formulario usará
        fields = ('username', 'first_name', 'last_name', 'email', 'rut', 'telefono')

    # --- VALIDACIONES DE FORMATO (Creación) ---

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if re.search(r'\d', data):
            raise ValidationError("El nombre no puede contener números.")
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if re.search(r'\d', data):
            raise ValidationError("El apellido no puede contener números.")
        return data

    def clean_rut(self):
        data = self.cleaned_data['rut']
        if not re.match(r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$', data):
            raise ValidationError("Formato de RUT incorrecto. Debe ser: 12.345.678-9")
        return data

    def clean_telefono(self):
        data = self.cleaned_data['telefono']
        if not re.match(r'^9\s\d{4}\s\d{4}$', data):
            raise ValidationError("Formato de Teléfono incorrecto. Debe ser: 9 1234 5678")
        return data
        
    # --- MÉTODO SAVE (Para hashear la contraseña) ---
    def save(self, commit=True):
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data["password"]) 
        if commit:
            user.save()
        return user

# --- 2. Formulario de EDICIÓN Personalizado ---
class CustomUserChangeForm(UserChangeForm):
    
    # --- Email como texto simple (requerido) ---
    email = forms.CharField(
        label='Correo (Requerido)', 
        max_length=254
    )
    
    # --- Campos con help_text para la EDICIÓN ---
    rut = forms.CharField(
        label='RUT', 
        max_length=12, 
        help_text='Formato: 12.345.678-9'
    )
    telefono = forms.CharField(
        label='Teléfono', 
        max_length=15, 
        help_text='Formato: 9 1234 5678'
    )
    
    class Meta:
        model = CustomUser
        fields = '__all__' # Usar todos los campos del modelo
    
    # --- VALIDACIONES DE FORMATO (Edición) ---
    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name', '')
        if re.search(r'\d', data):
            raise ValidationError("El nombre no puede contener números.")
        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name', '')
        if re.search(r'\d', data):
            raise ValidationError("El apellido no puede contener números.")
        return data

    def clean_rut(self):
        data = self.cleaned_data.get('rut', '')
        # Si el campo no es obligatorio en el modelo, permitimos que esté vacío
        if not data and self.instance.pk: # (Permite vacío al editar si ya existía)
            return data
        if not re.match(r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$', data):
            raise ValidationError("Formato de RUT incorrecto. Debe ser: 12.345.678-9")
        return data

    def clean_telefono(self):
        data = self.cleaned_data.get('telefono', '')
        if not data and self.instance.pk: # (Permite vacío al editar si ya existía)
            return data
        if not re.match(r'^9\s\d{4}\s\d{4}$', data):
            raise ValidationError("Formato de Teléfono incorrecto. Debe ser: 9 1234 5678")
        return data

# --- 3. Clase Admin (Corregida con la COMA) ---
class CustomUserAdmin(UserAdmin):
    # Formularios personalizados
    form = CustomUserChangeForm       # Para editar
    add_form = CustomUserCreationForm   # Para crear

    model = CustomUser
    
    # Fieldsets para EDITAR
    fieldsets = UserAdmin.fieldsets + (
        ('Datos Personales', {'fields': ('rut', 'telefono')}),
    )
    
    # Fieldsets para CREAR (con la coma)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
        ('Información Personal (Requerida)', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'rut', 'telefono', 'email'),
        }),
        (None, {
            'classes': ('wide',),
            'fields': ('password',), # <-- LA COMA MÁGICA
        }),
    )
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    

# Registrar
admin.site.register(CustomUser, CustomUserAdmin)