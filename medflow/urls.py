# formulario/urls.py
from django.contrib import admin
from django.urls import path, re_path
from anamnesis import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    # --- 1. Autenticación ---
    path('', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'), 

    # --- 2. Vistas de Menú ---
    path('menu/ambulancia/', views.menu_ambulancia, name='menu_ambulancia'),
    path('menu/recepcion/', views.menu_recepcion, name='menu_recepcion'),
    path('menu/supervisor/', views.menu_supervisor, name='menu_supervisor'),
    
    # --- 3. Vistas de Formularios ---
    path('formulario_ambulancia/', views.formulario_ambulancia, name='formulario_ambulancia'),
    re_path(r'^formulario/editar/(?P<form_id>[0-9a-f-]+)/$', views.editar_formulario_view, name='editar_formulario'),

    # --- 4. Vistas de Chat ---
    re_path(r'^chat/(?P<form_id>[0-9a-f-]+)/$', views.chat_formulario_view, name='chat_formulario'),

    # ====================================================================
    # --- 5. APIs (Endpoints para JavaScript/Fetch) ---
    # ====================================================================
    
    # --- APIs de Formularios (Crear / Actualizar) ---
    path('api/enviar_formulario/', views.enviar_formulario_ambulancia, name='enviar_formulario'),
    re_path(r'^api/formulario/actualizar/(?P<form_id>[0-9a-f-]+)/$', views.actualizar_formulario_view, name='api_actualizar_formulario'),

    # --- APIs del Panel de Recepción ---
    path('api/formularios_pendientes/', views.obtener_formularios_pendientes, name='obtener_formularios_pendientes'),
    path('api/formularios_aprobados/', views.obtener_formularios_aprobados, name='obtener_formularios_aprobados'),
    path('api/formulario_detalle/<uuid:form_id>/', views.obtener_detalle_formulario, name='obtener_detalle'),
    path('api/formulario/aprobar/', views.aprobar_formulario_view, name='aprobar_formulario'),
    path('api/formulario/solicitar_modificacion/', views.solicitar_modificacion_view, name='solicitar_modificacion'),
    
    # --- Ruta de Eliminación ---
    re_path(r'^api/formulario/eliminar/(?P<form_id>[0-9a-f-]+)/$', views.eliminar_formulario_view, name='eliminar_formulario'),

    # --- APIs de Bloqueo (En Revisión) ---
    path('api/formulario/bloquear/<str:form_id>/', views.bloquear_formulario_view, name='bloquear_formulario'),
    path('api/formulario/liberar/<str:form_id>/', views.liberar_formulario_view, name='liberar_formulario'),

    # --- API de Polling de Ambulancia ---
    path('api/formularios_ambulancia/', views.obtener_formularios_ambulancia, name='obtener_formularios_ambulancia'),

    # --- APIs del Chat ---
    re_path(r'^api/chat_mensajes/(?P<form_id>[0-9a-f-]+)/$', views.obtener_mensajes_chat, name='obtener_mensajes'),
    path('api/chat_enviar/', views.enviar_mensaje_chat, name='enviar_mensaje'),
    
    # +++ NUEVO API PARA MARCAR CHAT COMO LEÍDO +++
    re_path(r'^api/chat/marcar_leido/(?P<form_id>[0-9a-f-]+)/$', views.marcar_chat_leido, name='marcar_chat_leido'),

    # --- API de Auditoría ---
    re_path(r'^api/audit_logs/(?P<user_id>[0-9]+)/$', views.obtener_registros_auditoria, name='api_obtener_registros_auditoria'),
    
    # --- API para la nueva pestaña "Formularios" del Supervisor ---
    path('api/todos_los_formularios/', views.api_obtener_todos_los_formularios, name='api_obtener_todos_los_formularios'),
    
    # --- API para crear usuarios desde el panel de Supervisor ---
    path('api/supervisor/crear_usuario/', views.api_crear_usuario_view, name='api_crear_usuario'),
    
    
    # ==================================
    # INICIO DE LA MODIFICACIÓN
    # ==================================
    # APIs para Editar, Eliminar y Auditoría del Sistema
    path('api/supervisor/editar_usuario/<int:user_id>/', views.api_editar_usuario_view, name='api_editar_usuario'),
    path('api/supervisor/eliminar_usuario/<int:user_id>/', views.api_eliminar_usuario_view, name='api_eliminar_usuario'),
    path('api/sistema/todos_los_logs/', views.api_obtener_logs_del_sistema, name='api_obtener_logs_del_sistema'),
    # ==================================
    # FIN DE LA MODIFICACIÓN
    # ==================================


    # --- API de Exportación ---
    path('api/exportar_formulario/<str:form_id>/<str:formato>/', views.exportar_formulario_view, name='exportar_formulario'),

]