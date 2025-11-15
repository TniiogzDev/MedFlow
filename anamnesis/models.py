# formulario/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

# --- Importaciones para la corrección ---
from django.utils.translation import gettext_lazy as _
# No importamos el validador, porque justamente queremos quitarlo

# --- CustomUser ---
class CustomUser(AbstractUser):
    
    # --- INICIO DE LA CORRECCIÓN ---
    # Sobreescribimos el campo 'username' de AbstractUser
    # para quitar el validador estricto de caracteres.
    
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Requerido. 150 caracteres o menos. "
            "Letras, números y caracteres especiales permitidos." # Mensaje de ayuda actualizado
        ),
        #
        # La línea 'validators=[...]' que tenía AbstractUser se omite a propósito
        #
        error_messages={
            "unique": _("Este nombre de usuario ya existe."),
        },
    )
    # --- FIN DE LA CORRECCIÓN ---

    # Campos obligatorios que ya habías corregido
    rut = models.CharField(max_length=12, blank=False, null=False, verbose_name='RUT', unique=True)
    telefono = models.CharField(max_length=15, blank=False, null=False, verbose_name='Teléfono')
    
    # (El resto del modelo sigue igual)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    
    def __str__(self):
        return self.username

# --- Modelo de Formulario de Atención ---
class FormularioAtencion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="formularios_creados"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    
    # --- Estados Principales ---
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('REQUIERE_MODIFICACION', 'Requiere Modificacion'), 
        ('MODIFICADO', 'Modificado'), 
        ('APROBADO', 'Aprobado'),
    ]
    estado = models.CharField(max_length=25, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    aprobado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='formularios_aprobados'
    )
    
    # ==================================
    # INICIO DE LA MODIFICACIÓN
    # ==================================
    # Añadimos el campo para la fecha de aprobación
    aprobado_en = models.DateTimeField(blank=True, null=True)
    # ==================================
    # FIN DE LA MODIFICACIÓN
    # ==================================

    # --- Campos de Bloqueo Temporal ("En Revisión") ---
    revisado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='formularios_en_revision'
    )
    revisado_en = models.DateTimeField(blank=True, null=True)


    # --- Resto de campos del formulario ---
    nombre_paciente = models.CharField(max_length=200, blank=True, null=True)
    rut_paciente = models.CharField(max_length=12, blank=True, null=True)
    edad_paciente = models.IntegerField(blank=True, null=True)
    unidad_edad_paciente = models.CharField(max_length=10, default='Años') 
    sexo_paciente = models.CharField(max_length=10, blank=True, null=True) 
    presion_arterial = models.CharField(max_length=10, blank=True, null=True)
    frecuencia_cardiaca = models.IntegerField(blank=True, null=True)
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    saturacion_oxigeno = models.IntegerField(blank=True, null=True)
    glasgow = models.IntegerField(blank=True, null=True)
    motivo_consulta = models.TextField(blank=True, null=True)
    antecedentes = models.TextField(blank=True, null=True)
    tratamiento_administrado = models.TextField(blank=True, null=True)
    solicitudes_paciente = models.TextField(blank=True, null=True)
    triage = models.CharField(max_length=10, default='Verde') 
    instrucciones_recepcion = models.TextField(blank=True, null=True)
    eta_fecha = models.DateField(blank=True, null=True)
    eta_hora = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Caso {self.id.hex[:8]} - {self.nombre_paciente or 'N/N'}"
    
# --- MODELO PARA LOS MENSAJES DE CHAT ---
# (Este modelo no se modifica)
class MensajeChat(models.Model):
    formulario = models.ForeignKey(
        FormularioAtencion, 
        on_delete=models.CASCADE, 
        related_name="mensajes_chat"
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True
    )
    mensaje = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        autor_nombre = self.autor.username if self.autor else "Sistema"
        return f"Msg de {autor_nombre} en Form {self.formulario.id.hex[:8]}"

    class Meta:
        ordering = ['timestamp']