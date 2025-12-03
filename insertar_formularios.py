import os
import django
from django.utils import timezone
from datetime import timedelta
import random

# ====================================================================
# CONFIGURACIÓN DE ENTORNO DE DJANGO
# Asegúrate de que 'medflow.settings' coincida con tu configuración.
# ====================================================================
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medflow.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Asegúrate de que estos imports sean correctos para tu app 'anamnesis'
from anamnesis.models import FormularioAtencion, MensajeChat 

def generar_rut_formateado_aleatorio():
    """Genera un RUT chileno plausible con puntos y dígito verificador."""
    # Cuerpo del RUT (7 a 8 dígitos)
    rut_base_int = random.randint(1000000, 29999999)
    rut_body_str = str(rut_base_int)
    
    # Aplicar puntos de formato
    if len(rut_body_str) >= 8:
        # Formato XX.XXX.XXX
        cuerpo_formateado = f"{rut_body_str[:-7]}.{rut_body_str[-7:-4]}.{rut_body_str[-4:-1]}"
    else:
        # Formato X.XXX.XXX
        cuerpo_formateado = f"{rut_body_str[:-6]}.{rut_body_str[-6:-3]}.{rut_body_str[-3:]}"
    
    # Dígito verificador aleatorio (simplificado)
    rut_dv = random.choice(['K', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    
    return f"{cuerpo_formateado}-{rut_dv}"

def insertar_formularios_ejemplo():
    # --- 1. Definir roles y usuarios ---
    
    User = get_user_model()
    
    print("1. Buscando o creando grupos de roles...")
    try:
        ambulancia_group = Group.objects.get(name='Ambulancia')
    except Group.DoesNotExist:
        ambulancia_group = Group.objects.create(name='Ambulancia')
    
    try:
        recepcion_group = Group.objects.get(name='Recepcion')
    except Group.DoesNotExist:
        recepcion_group = Group.objects.create(name='Recepcion')
    
    # Usuario creador de formularios (AmbulanciaTest)
    try:
        user_ambulancia = User.objects.get(username='AmbulanciaTest')
        print("   - Usuario AmbulanciaTest encontrado.")
    except User.DoesNotExist:
        print("   - Creando usuario AmbulanciaTest...")
        user_ambulancia = User.objects.create_user(
            username='AmbulanciaTest', 
            password='testpassword',
            first_name='Ambulancia',
            last_name='Test',
            email='ambulancia@test.cl',
            rut=generar_rut_formateado_aleatorio(), # RUT FORMATO CORRECTO
            telefono='9 1111 2222'
        )
        user_ambulancia.groups.add(ambulancia_group)
    
    # Usuario para aprobar/gestionar formularios (RecepcionTest)
    try:
        user_recepcion = User.objects.get(username='RecepcionTest')
        print("   - Usuario RecepcionTest encontrado.")
    except User.DoesNotExist:
        print("   - Creando usuario RecepcionTest...")
        user_recepcion = User.objects.create_user(
            username='RecepcionTest', 
            password='testpassword',
            first_name='Recepcion',
            last_name='Test',
            email='recepcion@test.cl',
            rut=generar_rut_formateado_aleatorio(), # RUT FORMATO CORRECTO
            telefono='9 3333 4444'
        )
        user_recepcion.groups.add(recepcion_group)

    # --- 2. Preparar datos de ejemplo ---
    print("\n2. Preparando datos de 20 formularios...")

    ahora = timezone.now()
    pacientes = [
        "Ana García", "Benito López", "Carla Díaz", "David Ruiz", "Elena Pérez",
        "Felipe Castro", "Gloria Gómez", "Hugo Morales", "Irene Navarro", "Javier Soto",
        "Karina Silva", "Luis Torres", "Marta Vargas", "Néstor Yáñez", "Olga Zárate",
        "Pedro Alarcón", "Quimena Bustos", "Ramón Cáceres", "Sofía Espinoza", "Tomás Fuentes"
    ]
    
    # Define los estados que tendrá cada uno de los 20 formularios
    estados = [
        'PENDIENTE', 'PENDIENTE', 'MODIFICADO', 'REQUIERE_MODIFICACION', 'APROBADO',
        'PENDIENTE', 'MODIFICADO', 'PENDIENTE', 'REQUIERE_MODIFICACION', 'APROBADO',
        'PENDIENTE', 'MODIFICADO', 'PENDIENTE', 'REQUIERE_MODIFICACION', 'APROBADO',
        'PENDIENTE', 'PENDIENTE', 'PENDIENTE', 'APROBADO', 'MODIFICADO'
    ]
    
    triage_options = ['Rojo', 'Amarillo', 'Verde']
    prevision_options = ['FONASA', 'ISAPRE', 'PARTICULAR', 'OTRO']
    sexo_options = ['Hombre', 'Mujer']

    formularios_a_insertar = []

    for i in range(20):
        estado = estados[i]
        
        # Variar la fecha de creación (de 30 días atrás a hace unos minutos)
        dias_atras = random.randint(0, 30)
        creado_en_fecha = ahora - timedelta(days=dias_atras, minutes=random.randint(0, 1440))
        
        aprobado_en_fecha = None
        aprobado_por_user = None

        if estado == 'APROBADO':
            # La aprobación ocurre después de la creación
            aprobado_en_fecha = creado_en_fecha + timedelta(hours=random.randint(1, 24))
            aprobado_por_user = user_recepcion
        
        
        form_data = {
            'creado_por': user_ambulancia,
            'creado_en': creado_en_fecha,
            'estado': estado,
            'aprobado_por': aprobado_por_user,
            'aprobado_en': aprobado_en_fecha,
            
            # Datos del paciente (Todos son obligatorios en el frontend ahora)
            'nombre_paciente': pacientes[i],
            'rut_paciente': generar_rut_formateado_aleatorio(), # Usando la nueva función
            'edad_paciente': random.randint(1, 80),
            'unidad_edad_paciente': 'Años',
            'sexo_paciente': random.choice(sexo_options),
            'prevision': random.choice(prevision_options),
            'accidente_laboral': random.choice([True, False]),
            
            # Signos Vitales
            'presion_arterial': f"{random.randint(90, 160)}/{random.randint(60, 100)}",
            'frecuencia_cardiaca': random.randint(60, 120),
            'frecuencia_respiratoria': random.randint(12, 30),
            'temperatura': round(random.uniform(36.0, 38.5), 1),
            'saturacion_oxigeno': random.randint(88, 100),
            'glasgow': random.randint(10, 15),
            'llene_capilar': random.choice(['< 2 seg', '> 2 seg']),
            'score_mottling': random.randint(0, 5),
            'musculatura_accesoria': random.choice([True, False]),
            'fio2': random.randint(21, 50),
            
            # Anamnesis
            'motivo_consulta': f"Paciente {pacientes[i]} con dolor en cuadrante {i % 4 + 1}.",
            'antecedentes': f"Antecedentes de {random.choice(['HTA', 'Diabetes', 'Ninguno', 'Asma'])}.",
            'tratamiento_administrado': f"Paracetamol ({random.randint(500, 1000)}mg) y reposo.",
            'solicitudes_paciente': "Solicita manta y agua.",
            'funcionalidad': f"VGI {random.choice(['A', 'B'])}, EVF {random.randint(1, 4)}",
            'prestacion_requerida': "Traslado a Unidad de Urgencia.",
            
            # Notificación
            'triage': random.choice(triage_options),
            'instrucciones_recepcion': "Preparar box simple. Triage asignado: "+random.choice(triage_options),
            'eta_fecha': creado_en_fecha.date() + timedelta(days=1),
            'eta_hora': creado_en_fecha.time(),
        }
        formularios_a_insertar.append(form_data)

    # --- 3. Inserción de datos ---
    print("\n3. Insertando formularios en la base de datos...")
    
    formularios_creados_count = 0
    for data in formularios_a_insertar:
        # Crea y guarda el objeto en la base de datos
        FormularioAtencion.objects.create(**data)
        formularios_creados_count += 1
        
    print(f"\n✅ ¡Inserción exitosa! {formularios_creados_count} formularios de ejemplo creados.")

if __name__ == '__main__':
    insertar_formularios_ejemplo()